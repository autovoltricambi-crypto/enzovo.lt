import os
import json
import asyncio
from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from config import Config
from agent_simple import chat
from tools.cataloghi import browser_login_wp, browser_chiudi

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
    """Chiude il browser quando il server si spegne."""
    await browser_chiudi()

STATIC_DIR = Path(__file__).parent / "static"
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

conversazioni: dict[str, list] = {}


@app.get("/", response_class=HTMLResponse)
async def homepage():
    html_path = STATIC_DIR / "index.html"
    return HTMLResponse(html_path.read_text(encoding="utf-8"))


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
        conversazioni[session_id] = []

    coda: asyncio.Queue = asyncio.Queue()

    async def progress_callback(testo: str):
        await coda.put({"tipo": "progress", "testo": testo})

    async def esegui_chat():
        """Esegue la chat in background e mette il risultato finale in coda."""
        try:
            risposta, cronologia = await chat(
                messaggio,
                conversazioni[session_id],
                progress_callback=progress_callback,
            )
            conversazioni[session_id] = cronologia

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
    conversazioni[session_id] = []
    return JSONResponse({"successo": True})


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


if __name__ == "__main__":
    import uvicorn
    print(f"\nAgente Ricambi Auto — http://{Config.HOST}:{Config.PORT}\n")
    uvicorn.run(app, host=Config.HOST, port=Config.PORT)
