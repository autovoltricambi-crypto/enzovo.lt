"""Memoria persistente in JSON per ricerche, prodotti e note."""
import json
import os
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
