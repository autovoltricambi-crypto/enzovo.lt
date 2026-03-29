"""Memoria persistente in JSON per ricerche, prodotti e note."""
import json
import os
import re
from datetime import datetime
from config import Config


def _carica() -> dict:
    """Carica il file memoria.json, crea struttura vuota se non esiste."""
    if not os.path.exists(Config.MEMORIA_PATH):
        return {"ricerche": [], "prodotti": [], "note": [], "contesto_sito": {}}
    memoria = json.load(open(Config.MEMORIA_PATH, encoding="utf-8"))
    # Migrazione: aggiunge contesto_sito se mancante
    if "contesto_sito" not in memoria:
        memoria["contesto_sito"] = {}
    return memoria


def _salva(memoria: dict):
    """Salva la memoria su disco."""
    os.makedirs(os.path.dirname(Config.MEMORIA_PATH), exist_ok=True)
    with open(Config.MEMORIA_PATH, "w", encoding="utf-8") as f:
        json.dump(memoria, f, ensure_ascii=False, indent=2)


def salva_ricerca(query: str, catalogo: str, risultati_trovati: int) -> dict:
    """Salva una ricerca nella memoria storica."""
    memoria = _carica()
    memoria["ricerche"].append({
        "query": query,
        "catalogo": catalogo,
        "risultati": risultati_trovati,
        "data": datetime.now().isoformat(),
    })
    _salva(memoria)
    return {"successo": True, "ricerche_totali": len(memoria["ricerche"])}


def cerca_in_memoria(query: str, tipo: str | None = None) -> dict:
    """
    Cerca nelle ricerche, prodotti o note salvate.
    tipo: 'ricerche' | 'prodotti' | 'note' | None (cerca ovunque)
    """
    memoria = _carica()
    query_lower = query.lower()
    risultati = {}

    sezioni = [tipo] if tipo else ["ricerche", "prodotti", "note"]

    for sezione in sezioni:
        voci = memoria.get(sezione, [])
        trovati = []
        for v in voci:
            testo = json.dumps(v, ensure_ascii=False).lower()
            if query_lower in testo:
                trovati.append(v)
        if trovati:
            risultati[sezione] = trovati

    if not risultati:
        return {"trovato": False, "messaggio": f"Nessuna voce trovata per '{query}'"}

    return {"trovato": True, "risultati": risultati}


def salva_nota(titolo: str, contenuto: str) -> dict:
    """Salva una nota personale in memoria."""
    memoria = _carica()
    memoria["note"].append({
        "titolo": titolo,
        "contenuto": contenuto,
        "data": datetime.now().isoformat(),
    })
    _salva(memoria)
    return {"successo": True, "note_totali": len(memoria["note"])}


def aggiorna_contesto_sito(chiave: str, valore: str) -> dict:
    """
    Salva una coppia chiave-valore nel contesto permanente del sito.
    Persiste tra sessioni — usato dall'agente per ricordare decisioni e stato.

    Esempi:
      aggiorna_contesto_sito("margine_default", "35%")
      aggiorna_contesto_sito("categorie_create", "Filtri > Filtri Olio > BMW (ID 47)")
      aggiorna_contesto_sito("preferenze_utente", "Preferisce margine 35%, IVA 22%")
    """
    memoria = _carica()
    memoria["contesto_sito"][chiave] = {
        "valore": valore,
        "aggiornato": datetime.now().isoformat(),
    }
    _salva(memoria)
    return {"successo": True, "chiave": chiave, "valore": valore}


def leggi_contesto_sito(chiave: str | None = None) -> dict:
    """
    Legge il contesto del sito. Se chiave=None ritorna tutto il contesto.
    Usato dall'agente per recuperare decisioni e stato accumulati.
    """
    memoria = _carica()
    contesto = memoria.get("contesto_sito", {})
    if chiave:
        entry = contesto.get(chiave)
        if entry:
            return {"chiave": chiave, "valore": entry["valore"], "aggiornato": entry["aggiornato"]}
        return {"trovato": False, "chiave": chiave}
    return {"contesto": contesto}


def carica_contesto_agente() -> str:
    """
    Restituisce una stringa formattata con tutto il contesto del sito
    da iniettare nel system prompt dell'agente.
    """
    memoria = _carica()
    contesto = memoria.get("contesto_sito", {})

    if not contesto:
        return "Nessun contesto salvato ancora. Questo è l'inizio del progetto."

    righe = []
    for chiave, entry in contesto.items():
        valore = entry["valore"] if isinstance(entry, dict) else entry
        righe.append(f"- {chiave}: {valore}")

    # Aggiungi ultime 3 ricerche come contesto
    ricerche = memoria.get("ricerche", [])[-3:]
    if ricerche:
        righe.append("\nUltime ricerche effettuate:")
        for r in ricerche:
            righe.append(f"  - '{r['query']}' su {r['catalogo']} ({r['risultati']} risultati)")

    # Ultime 3 note
    note = memoria.get("note", [])[-3:]
    if note:
        righe.append("\nUltime note:")
        for n in note:
            righe.append(f"  - {n['titolo']}: {n['contenuto'][:100]}")

    return "\n".join(righe)


def lista_knowledge() -> dict:
    """Ritorna la lista dei file di knowledge disponibili in data/know/."""
    if not os.path.exists(Config.KNOW_DIR):
        return {"files": [], "messaggio": "Nessun file di knowledge trovato"}
    files = [f for f in sorted(os.listdir(Config.KNOW_DIR)) if f.endswith(".md")]
    return {"files": files, "path": Config.KNOW_DIR}


def leggi_knowledge(nome_file: str | None = None) -> dict:
    """
    Legge un file di knowledge da data/know/.
    Se nome_file è None, ritorna la lista dei file disponibili.
    """
    if not nome_file:
        return lista_knowledge()

    # Sicurezza: impedisci path traversal
    nome_file = os.path.basename(nome_file)
    percorso = os.path.join(Config.KNOW_DIR, nome_file)

    if not os.path.exists(percorso):
        disponibili = lista_knowledge()["files"]
        return {"errore": f"File '{nome_file}' non trovato. Disponibili: {disponibili}"}

    try:
        contenuto = open(percorso, encoding="utf-8").read()
        return {"file": nome_file, "contenuto": contenuto}
    except Exception as e:
        return {"errore": str(e)}


def aggiorna_knowledge(nome_file: str, contenuto: str) -> dict:
    """
    Sovrascrive un file di knowledge esistente in data/know/.
    Usato dall'agente per correggere informazioni errate segnalate dall'utente.
    nome_file: es. 'seo-ricambi-auto.md' (solo il nome, non il percorso)
    contenuto: nuovo contenuto completo del file in formato Markdown
    """
    # Sicurezza: impedisci path traversal
    nome_file = os.path.basename(nome_file)
    if not nome_file.endswith(".md"):
        return {"errore": "Solo file .md sono modificabili"}

    percorso = os.path.join(Config.KNOW_DIR, nome_file)

    if not os.path.exists(percorso):
        disponibili = lista_knowledge()["files"]
        return {"errore": f"File '{nome_file}' non trovato. Disponibili: {disponibili}"}

    try:
        with open(percorso, "w", encoding="utf-8") as f:
            f.write(contenuto)
        return {
            "successo": True,
            "file": nome_file,
            "caratteri": len(contenuto),
            "messaggio": f"File '{nome_file}' aggiornato correttamente",
        }
    except Exception as e:
        return {"errore": str(e)}


def crea_knowledge(nome_file: str, contenuto: str) -> dict:
    """
    Crea un nuovo file di knowledge in data/know/.
    nome_file: es. 'nuovo-argomento.md' (solo il nome, non il percorso)
    contenuto: contenuto del file in formato Markdown
    """
    nome_file = os.path.basename(nome_file)
    if not nome_file.endswith(".md"):
        return {"errore": "Solo file .md sono supportati"}

    os.makedirs(Config.KNOW_DIR, exist_ok=True)
    percorso = os.path.join(Config.KNOW_DIR, nome_file)

    if os.path.exists(percorso):
        return {"errore": f"File '{nome_file}' esiste già. Usa aggiorna_knowledge per modificarlo."}

    try:
        with open(percorso, "w", encoding="utf-8") as f:
            f.write(contenuto)
        return {
            "successo": True,
            "file": nome_file,
            "caratteri": len(contenuto),
            "messaggio": f"File '{nome_file}' creato correttamente",
        }
    except Exception as e:
        return {"errore": str(e)}


def carica_conoscenze() -> str:
    """
    Carica tutti i file .md da data/know/ e li concatena in una stringa
    da iniettare nel system prompt dell'agente.

    Puoi aggiungere, modificare o rimuovere file in data/know/ per
    aggiornare l'expertise dell'agente senza toccare il codice.
    """
    if not os.path.exists(Config.KNOW_DIR):
        return ""

    sezioni = []
    for nome_file in sorted(os.listdir(Config.KNOW_DIR)):
        if not nome_file.endswith(".md"):
            continue
        percorso = os.path.join(Config.KNOW_DIR, nome_file)
        try:
            contenuto = open(percorso, encoding="utf-8").read().strip()
            if contenuto:
                sezioni.append(contenuto)
        except Exception:
            continue

    return "\n\n---\n\n".join(sezioni)


def statistiche_memoria() -> dict:
    """Ritorna statistiche sulla memoria."""
    memoria = _carica()
    return {
        "ricerche": len(memoria.get("ricerche", [])),
        "prodotti": len(memoria.get("prodotti", [])),
        "note": len(memoria.get("note", [])),
        "file": Config.MEMORIA_PATH,
        "esiste": os.path.exists(Config.MEMORIA_PATH),
    }


# ==========================================
# PROFILO UTENTE
# ==========================================

PROFILO_PATH = os.path.join(Config.DATA_DIR, "profilo.json")

_PROFILO_DEFAULT = {
    "nome": "",
    "attivita": "",
    "settore": "",
    "sito_web": "",
    "indirizzo": "",
    "citta": "",
    "stack_tecnico": "",
    "preferenze_tecniche": "",
    "budget_mensile": "",
    "obiettivo_principale": "",
    "preferenze": "",
    "note_personali": "",
}


def carica_profilo() -> dict:
    """Carica il profilo utente da disco. Crea il file con valori vuoti se non esiste."""
    if not os.path.exists(PROFILO_PATH):
        return dict(_PROFILO_DEFAULT)
    try:
        with open(PROFILO_PATH, encoding="utf-8") as f:
            profilo = json.load(f)
        # Merge con default per campi nuovi
        merged = dict(_PROFILO_DEFAULT)
        merged.update(profilo)
        return merged
    except Exception:
        return dict(_PROFILO_DEFAULT)


def aggiorna_profilo(**kwargs) -> dict:
    """
    Aggiorna uno o più campi del profilo utente.
    Accetta qualsiasi chiave — i campi standard sono:
    nome, attivita, settore, budget_mensile, obiettivo_principale, preferenze, note_personali.
    Puoi aggiungere campi custom.
    """
    profilo = carica_profilo()
    campi_aggiornati = []
    for chiave, valore in kwargs.items():
        if valore is not None and str(valore).strip():
            profilo[chiave] = str(valore).strip()
            campi_aggiornati.append(chiave)
    os.makedirs(os.path.dirname(PROFILO_PATH), exist_ok=True)
    with open(PROFILO_PATH, "w", encoding="utf-8") as f:
        json.dump(profilo, f, ensure_ascii=False, indent=2)
    return {"successo": True, "campi_aggiornati": campi_aggiornati, "profilo": profilo}


def _merge_valori_unici(valore_corrente: str, nuovi_valori: list[str]) -> str:
    """Unisce valori testuali evitando duplicati e preservando l'ordine."""
    visti = set()
    output = []

    for raw in (valore_corrente.split(",") if valore_corrente else []):
        item = raw.strip()
        if item and item.lower() not in visti:
            visti.add(item.lower())
            output.append(item)

    for raw in nuovi_valori:
        item = str(raw).strip()
        if item and item.lower() not in visti:
            visti.add(item.lower())
            output.append(item)

    return ", ".join(output)


def auto_aggiorna_profilo_da_testo(testo: str) -> dict:
    """
    Estrae automaticamente dal messaggio utente informazioni stabili di profilo,
    incluse stack e preferenze tecniche emerse in chat.
    """
    if not testo or not testo.strip():
        return {"successo": True, "campi_aggiornati": [], "profilo": carica_profilo()}

    originale = testo.strip()
    lower = originale.lower()
    profilo = carica_profilo()
    updates = {}

    if any(k in lower for k in ("mio sito", "nostro sito", "il sito si chiama", "sito si chiama", "negozio", "azienda")):
        match_sito = re.search(r"(https?://[^\s,;]+|(?:[a-z0-9-]+\.)+[a-z]{2,})", originale, re.IGNORECASE)
        if match_sito:
            sito = match_sito.group(1).rstrip(".,;)")
            if not sito.startswith(("http://", "https://")):
                sito = f"https://{sito}"
            updates["sito_web"] = sito

    match_citta = re.search(r"\bsi trova a\s+([A-Za-zÀ-ÿ'\- ]+?)\s+in\s+(via|viale|piazza|corso)\b", originale, re.IGNORECASE)
    if match_citta:
        updates["citta"] = match_citta.group(1).strip().title()

    match_indirizzo = re.search(
        r"\b(via|viale|piazza|corso)\s+[A-Za-zÀ-ÿ0-9'\.\-\s]+?\s+\d+[A-Za-z0-9/\-]*",
        originale,
        re.IGNORECASE,
    )
    if match_indirizzo:
        indirizzo = re.sub(r"\s+", " ", match_indirizzo.group(0).strip())
        parts = indirizzo.split(" ")
        if parts:
            parts[0] = parts[0].capitalize()
        updates["indirizzo"] = " ".join(parts)

    stack_map = {
        r"\bwordpress\b": "WordPress",
        r"\bwoocommerce\b": "WooCommerce",
        r"\belementor\b": "Elementor",
        r"\bhtml\b": "HTML",
        r"\bcss\b": "CSS",
        r"\bjavascript\b|\bjs\b": "JavaScript",
        r"\bphp\b": "PHP",
        r"\bpython\b": "Python",
        r"\bfastapi\b": "FastAPI",
        r"\bbrowser-use\b": "browser-use",
        r"\bplaywright\b": "Playwright",
    }
    stack_nuovo = []
    for pattern, label in stack_map.items():
        if re.search(pattern, lower, re.IGNORECASE):
            stack_nuovo.append(label)
    if stack_nuovo:
        updates["stack_tecnico"] = _merge_valori_unici(profilo.get("stack_tecnico", ""), stack_nuovo)

    preferenze_nuove = []
    if any(k in lower for k in ("responsive", "cellulare", "smartphone", "mobile-first", "mobile first")):
        preferenze_nuove.append("responsive mobile-first")
    if any(k in lower for k in ("headless false", "browser visibile", "vedere il browser")):
        preferenze_nuove.append("browser visibile per debug")
    if any(k in lower for k in ("draft", "bozza prima", "prima in bozza")):
        preferenze_nuove.append("pubblicazione in draft prima del publish")
    if any(k in lower for k in ("categorie blog", "categoria blog", "archivio blog", "pagina blog")):
        preferenze_nuove.append("blog organizzato per categorie")
    if preferenze_nuove:
        updates["preferenze_tecniche"] = _merge_valori_unici(profilo.get("preferenze_tecniche", ""), preferenze_nuove)

    if not updates:
        return {"successo": True, "campi_aggiornati": [], "profilo": profilo}

    return aggiorna_profilo(**updates)


# ==========================================
# TRACCIAMENTO PRODOTTI
# ==========================================

def salva_prodotto_in_memoria(prodotto: dict) -> dict:
    """
    Salva un prodotto nella memoria locale quando viene creato su WooCommerce.
    Chiamata automaticamente dopo crea_prodotto e importa_prodotti_bulk.
    """
    memoria = _carica()
    if "prodotti" not in memoria:
        memoria["prodotti"] = []
    memoria["prodotti"].append({
        **prodotto,
        "data_creazione": datetime.now().isoformat(),
    })
    _salva(memoria)
    return {"successo": True, "prodotti_in_memoria": len(memoria["prodotti"])}


# ==========================================
# RIEPILOGO SESSIONE
# ==========================================

SESSIONI_DIR = os.path.join(Config.DATA_DIR, "sessioni")


def salva_riepilogo_sessione(session_id: str, messaggi_utente: int, messaggi_agente: int, riepilogo: str) -> dict:
    """
    Salva un riepilogo della sessione su disco.
    Chiamata quando l'utente resetta la chat o il server si spegne.
    """
    os.makedirs(SESSIONI_DIR, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    nome_file = f"{session_id}_{timestamp}.json"
    percorso = os.path.join(SESSIONI_DIR, nome_file)

    sessione = {
        "session_id": session_id,
        "data": datetime.now().isoformat(),
        "messaggi_utente": messaggi_utente,
        "messaggi_agente": messaggi_agente,
        "riepilogo": riepilogo,
    }

    with open(percorso, "w", encoding="utf-8") as f:
        json.dump(sessione, f, ensure_ascii=False, indent=2)

    return {"successo": True, "file": nome_file}


def carica_ultimi_riepiloghi(n: int = 3) -> list:
    """Carica gli ultimi N riepiloghi di sessione per iniettarli nel contesto."""
    if not os.path.exists(SESSIONI_DIR):
        return []
    files = sorted(
        [f for f in os.listdir(SESSIONI_DIR) if f.endswith(".json")],
        reverse=True,
    )[:n]
    riepiloghi = []
    for f in files:
        try:
            with open(os.path.join(SESSIONI_DIR, f), encoding="utf-8") as fh:
                riepiloghi.append(json.load(fh))
        except Exception:
            continue
    return riepiloghi


# ==========================================
# CONVERSAZIONI PERSISTENTI
# ==========================================

CONVERSAZIONI_DIR = os.path.join(Config.DATA_DIR, "conversazioni")


def salva_conversazione(session_id: str, cronologia: list) -> None:
    """Salva la cronologia di una conversazione su disco."""
    if not cronologia:
        return
    os.makedirs(CONVERSAZIONI_DIR, exist_ok=True)
    percorso = os.path.join(CONVERSAZIONI_DIR, f"{session_id}.json")
    with open(percorso, "w", encoding="utf-8") as f:
        json.dump(cronologia, f, ensure_ascii=False)


def carica_conversazione(session_id: str) -> list:
    """Carica una conversazione da disco. Ritorna lista vuota se non esiste."""
    percorso = os.path.join(CONVERSAZIONI_DIR, f"{session_id}.json")
    if not os.path.exists(percorso):
        return []
    try:
        with open(percorso, encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []
