import os
import json
import asyncio
import csv
from io import BytesIO
from pathlib import Path
from fastapi import FastAPI, Request, UploadFile, File, Form
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from config import Config
from agent_simple import chat
from tools.cataloghi import browser_login_wp, browser_chiudi
from tools.memoria import salva_conversazione, carica_conversazione, salva_riepilogo_sessione

Config.validate()

app = FastAPI(title="Agente Ricambi Auto")


@app.on_event("startup")
async def startup():
    """Avvia il browser persistente e fa il login WP all'avvio del server."""
    print("Avvio browser persistente e login WordPress...")
    ok = await browser_login_wp()
    if ok:
        print("Browser pronto, login WP completato.")
    else:
        print("Browser avviato (login WP non riuscito — controllare credenziali .env)")


@app.on_event("shutdown")
async def shutdown():
    """Salva tutte le conversazioni e chiude il browser."""
    for sid, cron in conversazioni.items():
        if cron:
            _salva_riepilogo_da_cronologia(sid, cron)
            salva_conversazione(sid, cron)
    await browser_chiudi()

STATIC_DIR = Path(__file__).parent / "static"
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

conversazioni: dict[str, list] = {}
allegati_sessione: dict[str, list] = {}

UPLOADS_DIR = Path(Config.DATA_DIR) / "uploads"
UPLOADS_DIR.mkdir(parents=True, exist_ok=True)
MAX_UPLOAD_BYTES = 10 * 1024 * 1024
SUPPORTED_EXTENSIONS = {".csv", ".pdf"}


def _salva_riepilogo_da_cronologia(session_id: str, cronologia: list) -> None:
    """Estrae un riepilogo dalla cronologia e lo salva su disco."""
    msg_utente = sum(1 for m in cronologia if m.get("role") == "user" and isinstance(m.get("content"), str))
    msg_agente = sum(1 for m in cronologia if m.get("role") == "assistant" and isinstance(m.get("content"), str))
    if msg_utente == 0:
        return
    # Prendi gli ultimi messaggi di testo per costruire un riepilogo semplice
    ultimi = []
    for m in cronologia[-6:]:
        c = m.get("content", "")
        if isinstance(c, str) and c.strip():
            role = "Utente" if m["role"] == "user" else "Agente"
            ultimi.append(f"{role}: {c[:150]}")
    riepilogo = " | ".join(ultimi) if ultimi else "Sessione senza contenuto testuale."
    salva_riepilogo_sessione(session_id, msg_utente, msg_agente, riepilogo)


def _ripulisci_cronologia_corrotta(cronologia: list) -> None:
    """Rimuove tool_use blocks senza tool_result corrispondente dalla cronologia.
    Chiamata automaticamente quando l'API Anthropic restituisce un 400 per questa causa.
    """
    for i in range(len(cronologia) - 1, -1, -1):
        msg = cronologia[i]
        if msg.get("role") == "assistant":
            content = msg.get("content", [])
            has_tool_use = (
                isinstance(content, list)
                and any(getattr(b, "type", None) == "tool_use" or
                        (isinstance(b, dict) and b.get("type") == "tool_use")
                        for b in content)
            )
            if has_tool_use and i + 1 >= len(cronologia):
                cronologia.pop(i)
            break


def _estrai_testo_csv(raw_bytes: bytes, max_rows: int = 80) -> str:
    """Estrae un'anteprima testuale da un CSV per darlo in pasto al modello."""
    decode_error = None
    contenuto = ""
    for enc in ("utf-8-sig", "utf-8", "latin-1"):
        try:
            contenuto = raw_bytes.decode(enc)
            decode_error = None
            break
        except Exception as e:
            decode_error = e

    if decode_error is not None:
        raise ValueError("Impossibile decodificare il file CSV") from decode_error

    sample = contenuto[:4096]
    try:
        dialect = csv.Sniffer().sniff(sample, delimiters=";,\t,")
        sep = dialect.delimiter
    except Exception:
        sep = ";" if ";" in sample else ","

    rows = list(csv.reader(contenuto.splitlines(), delimiter=sep))
    if not rows:
        return "CSV vuoto."

    header = rows[0]
    body = rows[1:max_rows + 1]
    lines = [
        f"CSV con separatore '{sep}'",
        f"Colonne ({len(header)}): {', '.join(str(c) for c in header)}",
        f"Righe totali (escluso header): {max(0, len(rows) - 1)}",
        "Anteprima righe:",
    ]

    for idx, row in enumerate(body, start=1):
        row_txt = " | ".join(str(cell).strip() for cell in row)
        lines.append(f"{idx}. {row_txt}")

    return "\n".join(lines)


def _estrai_testo_pdf(raw_bytes: bytes, max_chars: int = 18000) -> str:
    """Estrae testo dai PDF con fallback su pagine senza testo."""
    from pypdf import PdfReader

    reader = PdfReader(BytesIO(raw_bytes))
    estratti: list[str] = []
    for i, page in enumerate(reader.pages, start=1):
        txt = (page.extract_text() or "").strip()
        if txt:
            estratti.append(f"--- Pagina {i} ---\n{txt}")

    if not estratti:
        return (
            "PDF senza testo estraibile. Potrebbe essere una scansione o contenere solo immagini. "
            "Se serve OCR, va aggiunto un modulo dedicato."
        )

    full_text = "\n\n".join(estratti)
    if len(full_text) > max_chars:
        full_text = full_text[:max_chars] + "\n\n[... testo PDF troncato ...]"
    return full_text


def _context_allegati_da_iniettare(session_id: str) -> tuple[str, list[int]]:
    """Ritorna il contesto file non ancora usato in chat per questa sessione."""
    allegati = allegati_sessione.get(session_id, [])
    pending = [
        (i, a)
        for i, a in enumerate(allegati)
        if not a.get("usato_in_chat")
    ]
    if not pending:
        return "", []

    blocchi = []
    idx_pending = []
    for i, item in pending:
        idx_pending.append(i)
        blocchi.append(
            "\n".join([
                f"File: {item['filename']}",
                f"Tipo: {item['type']}",
                "Contenuto estratto:",
                item["text"],
            ])
        )

    context = (
        "[CONTESTO FILE ALLEGATI]\n"
        + "\n\n".join(blocchi)
        + "\n[Fine contesto allegati]"
    )
    return context, idx_pending


@app.get("/", response_class=HTMLResponse)
async def homepage():
    html_path = STATIC_DIR / "index.html"
    return HTMLResponse(html_path.read_text(encoding="utf-8"))


@app.post("/api/upload")
async def api_upload(session_id: str = Form(...), file: UploadFile = File(...)):
    if not session_id.strip():
        return JSONResponse({"errore": "session_id mancante"}, status_code=400)

    filename = (file.filename or "").strip()
    if not filename:
        return JSONResponse({"errore": "Nome file non valido"}, status_code=400)

    ext = Path(filename).suffix.lower()
    if ext not in SUPPORTED_EXTENSIONS:
        return JSONResponse(
            {"errore": "Formato non supportato. Usa solo file CSV o PDF."},
            status_code=400,
        )

    raw = await file.read()
    if not raw:
        return JSONResponse({"errore": "File vuoto"}, status_code=400)
    if len(raw) > MAX_UPLOAD_BYTES:
        return JSONResponse(
            {"errore": "File troppo grande (max 10MB)"},
            status_code=400,
        )

    try:
        if ext == ".csv":
            extracted = _estrai_testo_csv(raw)
            file_type = "csv"
        else:
            extracted = _estrai_testo_pdf(raw)
            file_type = "pdf"
    except Exception as e:
        return JSONResponse(
            {"errore": f"Impossibile leggere il file: {e}"},
            status_code=400,
        )

    safe_name = Path(filename).name.replace(" ", "_")
    ts = asyncio.get_running_loop().time()
    storage_name = f"{session_id}_{int(ts * 1000)}_{safe_name}"
    storage_path = UPLOADS_DIR / storage_name
    storage_path.write_bytes(raw)

    if session_id not in allegati_sessione:
        allegati_sessione[session_id] = []

    file_id = f"f_{len(allegati_sessione[session_id]) + 1}_{int(ts * 1000)}"
    allegati_sessione[session_id].append({
        "id": file_id,
        "filename": filename,
        "type": file_type,
        "size_bytes": len(raw),
        "path": str(storage_path),
        "text": extracted,
        "usato_in_chat": False,
    })

    preview = extracted[:450] + ("..." if len(extracted) > 450 else "")
    return JSONResponse({
        "successo": True,
        "file_id": file_id,
        "filename": filename,
        "tipo": file_type,
        "dimensione_kb": round(len(raw) / 1024, 1),
        "preview": preview,
    })


@app.post("/api/chat")
async def api_chat(request: Request):
    """
    Endpoint chat con Server-Sent Events.

    Manda eventi nel formato SSE:
      data: {"tipo": "progress", "testo": "..."}
      data: {"tipo": "risposta", "testo": "...", "csv_disponibile": "..."}
      data: {"tipo": "errore", "testo": "..."}

    Il frontend legge questi eventi con EventSource o fetch + ReadableStream
    e li mostra in tempo reale nella chat.
    """
    data = await request.json()
    messaggio = data.get("messaggio", "").strip()
    session_id = data.get("session_id", "default")

    if not messaggio:
        return JSONResponse({"errore": "Messaggio vuoto"}, status_code=400)

    if session_id not in conversazioni:
        conversazioni[session_id] = carica_conversazione(session_id)

    if session_id not in allegati_sessione:
        allegati_sessione[session_id] = []

    context_allegati, pending_idx = _context_allegati_da_iniettare(session_id)
    messaggio_input = (
        f"{context_allegati}\n\nMessaggio utente:\n{messaggio}"
        if context_allegati
        else messaggio
    )

    coda: asyncio.Queue = asyncio.Queue()

    async def progress_callback(testo: str):
        await coda.put({"tipo": "progress", "testo": testo})

    async def esegui_chat():
        """Esegue la chat in background e mette il risultato finale in coda."""
        try:
            risposta, cronologia = await chat(
                messaggio_input,
                conversazioni[session_id],
                progress_callback=progress_callback,
            )
            conversazioni[session_id] = cronologia
            salva_conversazione(session_id, cronologia)

            for i in pending_idx:
                if i < len(allegati_sessione.get(session_id, [])):
                    allegati_sessione[session_id][i]["usato_in_chat"] = True

            csv_file = None
            if "exports/" in risposta or ".csv" in risposta:
                exports = sorted(
                    Path(Config.EXPORTS_DIR).glob("*.csv"),
                    key=os.path.getctime,
                    reverse=True,
                )
                if exports:
                    csv_file = exports[0].name

            await coda.put({
                "tipo": "risposta",
                "testo": risposta,
                "csv_disponibile": csv_file,
            })
        except Exception as e:
            # Se la cronologia è corrotta (tool_use senza tool_result), ripuliscila
            # così il prossimo messaggio funziona normalmente
            if "tool_use" in str(e) and "tool_result" in str(e):
                _ripulisci_cronologia_corrotta(conversazioni.get(session_id, []))
            await coda.put({"tipo": "errore", "testo": str(e)})

    async def sse_generator():
        """Generator SSE: legge dalla coda e manda eventi al browser."""
        task = asyncio.create_task(esegui_chat())

        while True:
            try:
                evento = await asyncio.wait_for(coda.get(), timeout=120)
                yield f"data: {json.dumps(evento, ensure_ascii=False)}\n\n"

                if evento["tipo"] in ("risposta", "errore"):
                    break
            except asyncio.TimeoutError:
                yield 'data: {"tipo": "ping"}\n\n'

        await task

    return StreamingResponse(
        sse_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
        },
    )


@app.post("/api/reset")
async def api_reset(request: Request):
    data = await request.json()
    session_id = data.get("session_id", "default")
    cron = conversazioni.get(session_id, [])
    if cron:
        _salva_riepilogo_da_cronologia(session_id, cron)
    conversazioni[session_id] = []
    allegati_sessione[session_id] = []
    salva_conversazione(session_id, [])
    return JSONResponse({"successo": True})


@app.get("/api/csv-index")
async def api_csv_index():
    """Ritorna l'indice dei CSV salvati con descrizione."""
    from tools.csv_export import lista_csv_salvati
    return JSONResponse(lista_csv_salvati())


@app.get("/api/downloads")
async def api_downloads():
    if not os.path.exists(Config.EXPORTS_DIR):
        return JSONResponse({"files": []})
    files = []
    for f in sorted(os.listdir(Config.EXPORTS_DIR), reverse=True):
        if f.endswith(".csv"):
            path = os.path.join(Config.EXPORTS_DIR, f)
            files.append({
                "nome": f,
                "dimensione_kb": round(os.path.getsize(path) / 1024, 1),
            })
    return JSONResponse({"files": files})


@app.get("/api/download/{filename}")
async def api_download(filename: str):
    filepath = os.path.join(Config.EXPORTS_DIR, filename)
    if not os.path.exists(filepath) or not filename.endswith(".csv"):
        return JSONResponse({"errore": "File non trovato"}, status_code=404)
    return FileResponse(
        filepath,
        media_type="text/csv",
        filename=filename,
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )


@app.get("/api/memoria")
async def api_memoria():
    from tools.memoria import statistiche_memoria
    return JSONResponse(statistiche_memoria())


@app.get("/api/debug/config")
async def debug_config():
    """Mostra la configurazione caricata dal .env (password oscurate)."""
    portali = {}
    for nome, info in Config.PORTALI_B2B.items():
        portali[nome] = {
            "url": info["url"] or "❌ VUOTO",
            "user": info["user"] or "❌ VUOTO",
            "password": "***" if info["password"] else "❌ VUOTO",
        }
    return JSONResponse({
        "wp_url": Config.WP_URL or "❌ VUOTO",
        "wp_user": Config.WP_USER or "❌ VUOTO",
        "portali": portali,
    })


@app.get("/api/debug/browser")
async def debug_browser():
    """Testa browser-use direttamente e ritorna l'errore grezzo senza filtri."""
    import traceback
    risultato: dict = {"versioni": {}, "test": None, "errore": None}

    for pkg in ("browser_use", "langchain_anthropic", "playwright"):
        try:
            mod = __import__(pkg)
            risultato["versioni"][pkg] = getattr(mod, "__version__", "installato")
        except Exception as e:
            risultato["versioni"][pkg] = f"NON TROVATO: {e}"

    try:
        from browser_use import Agent, Browser, BrowserProfile, ChatAnthropic
        llm = ChatAnthropic(
            model="claude-haiku-4-5-20251001",
            api_key=Config.ANTHROPIC_API_KEY,
        )
        browser = Browser(browser_profile=BrowserProfile(headless=False))
        agent = Agent(
            task="Vai su https://example.com e dimmi il titolo della pagina.",
            llm=llm,
            browser=browser,
        )
        history = await agent.run(max_steps=3)
        risultato["test"] = history.final_result() or "Completato senza risultato"
    except Exception:
        risultato["errore"] = traceback.format_exc()

    return JSONResponse(risultato)


@app.get("/api/obiettivi")
async def api_obiettivi():
    """Ritorna tutti gli obiettivi attivi con i loro task."""
    from tools.obiettivi import lista_obiettivi
    return JSONResponse(lista_obiettivi(solo_attivi=True))


@app.get("/api/obiettivi/oggi")
async def api_priorita_oggi():
    """Ritorna i 3 task più urgenti da fare oggi."""
    from tools.obiettivi import priorita_oggi
    return JSONResponse(priorita_oggi())


@app.get("/api/obiettivi/statistiche")
async def api_statistiche_obiettivi():
    """Ritorna statistiche generali sugli obiettivi."""
    from tools.obiettivi import statistiche_obiettivi
    return JSONResponse(statistiche_obiettivi())


@app.get("/api/gamification")
async def api_gamification():
    """Ritorna punteggio XP, streak e achievement."""
    from tools.obiettivi import stato_gamification
    return JSONResponse(stato_gamification())


@app.get("/api/sessioni")
async def api_sessioni():
    """Ritorna tutti i riepiloghi sessione ordinati dal più recente."""
    from tools.memoria import SESSIONI_DIR
    import os, json
    if not os.path.exists(SESSIONI_DIR):
        return JSONResponse({"sessioni": []})
    files = sorted(
        [f for f in os.listdir(SESSIONI_DIR) if f.endswith(".json")],
        reverse=True,
    )
    sessioni = []
    for f in files:
        try:
            with open(os.path.join(SESSIONI_DIR, f), encoding="utf-8") as fh:
                sessioni.append(json.load(fh))
        except Exception:
            continue
    return JSONResponse({"sessioni": sessioni})


if __name__ == "__main__":
    import uvicorn
    print(f"\nAgente Ricambi Auto — http://{Config.HOST}:{Config.PORT}\n")
    uvicorn.run(app, host=Config.HOST, port=Config.PORT)
