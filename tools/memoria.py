"""Memoria persistente in JSON per ricerche, prodotti e note."""
import json
import os
from datetime import datetime
from config import Config


def _carica() -> dict:
    """Carica il file memoria.json, crea struttura vuota se non esiste."""
    if not os.path.exists(Config.MEMORIA_PATH):
        return {"ricerche": [], "prodotti": [], "note": []}
    with open(Config.MEMORIA_PATH, encoding="utf-8") as f:
        return json.load(f)


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
