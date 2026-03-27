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


def cerca_in_memoria(query: str, tipo: str = None) -> dict:
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


def leggi_contesto_sito(chiave: str = None) -> dict:
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
