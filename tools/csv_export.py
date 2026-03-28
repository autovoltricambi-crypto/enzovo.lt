"""Esportazione risultati in CSV compatibile con Excel italiano."""
import csv
import json
import os
from datetime import datetime
from config import Config

CSV_INDEX_PATH = os.path.join(Config.DATA_DIR, "csv_index.json")


def _carica_index() -> list:
    if not os.path.exists(CSV_INDEX_PATH):
        return []
    with open(CSV_INDEX_PATH, encoding="utf-8") as f:
        return json.load(f)


def _salva_index(index: list):
    os.makedirs(os.path.dirname(CSV_INDEX_PATH), exist_ok=True)
    with open(CSV_INDEX_PATH, "w", encoding="utf-8") as f:
        json.dump(index, f, ensure_ascii=False, indent=2)


def lista_csv_salvati() -> dict:
    """Ritorna l'indice di tutti i CSV salvati con descrizione e data."""
    index = _carica_index()
    return {"csv": index, "totale": len(index)}


def esporta_csv(prodotti: list, nome_file: str = None, descrizione: str = "") -> dict:
    """
    Esporta una lista di prodotti in CSV con separatore `;` (Excel italiano).
    Salva il file nella directory exports/ e ritorna il percorso.
    """
    if not prodotti:
        return {"errore": "Nessun prodotto da esportare"}

    if not nome_file:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        nome_file = f"ricerca_{timestamp}"

    # Assicura estensione .csv
    if not nome_file.endswith(".csv"):
        nome_file += ".csv"

    percorso = os.path.join(Config.EXPORTS_DIR, nome_file)

    # Ricava le colonne dai dati (unione di tutte le chiavi presenti)
    colonne = []
    for p in prodotti:
        for k in p.keys():
            if k not in colonne:
                colonne.append(k)

    with open(percorso, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=colonne, delimiter=";", extrasaction="ignore")
        writer.writeheader()
        writer.writerows(prodotti)

    dimensione_kb = round(os.path.getsize(percorso) / 1024, 1)

    # Salva nell'indice CSV
    index = _carica_index()
    index.append({
        "file": nome_file,
        "descrizione": descrizione or nome_file,
        "righe": len(prodotti),
        "dimensione_kb": dimensione_kb,
        "data": datetime.now().isoformat(),
    })
    _salva_index(index)

    return {
        "successo": True,
        "file": nome_file,
        "percorso": percorso,
        "righe": len(prodotti),
        "dimensione_kb": dimensione_kb,
    }
