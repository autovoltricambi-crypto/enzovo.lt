"""Esportazione risultati in CSV compatibile con Excel italiano."""
import csv
import os
from datetime import datetime
from config import Config


def esporta_csv(prodotti: list, nome_file: str = None) -> dict:
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

    return {
        "successo": True,
        "file": nome_file,
        "percorso": percorso,
        "righe": len(prodotti),
        "dimensione_kb": dimensione_kb,
    }
