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


# ==========================================
# LETTURA E MODIFICA CSV
# ==========================================

def _rileva_separatore(percorso: str) -> str:
    """Rileva il separatore del CSV (`;` o `,`)."""
    with open(percorso, encoding="utf-8-sig") as f:
        prima_riga = f.readline()
    if ";" in prima_riga:
        return ";"
    return ","


def leggi_csv(nome_file: str, limite_righe: int = 50) -> dict:
    """
    Legge un CSV dalla cartella exports/ e ritorna colonne + righe.
    nome_file: nome del file (es: 'prodotti_r304.csv')
    limite_righe: max righe da ritornare (default 50, 0 = tutte)
    """
    nome_file = os.path.basename(nome_file)
    percorso = os.path.join(Config.EXPORTS_DIR, nome_file)

    if not os.path.exists(percorso):
        disponibili = [f for f in os.listdir(Config.EXPORTS_DIR) if f.endswith(".csv")]
        return {"errore": f"File '{nome_file}' non trovato. Disponibili: {disponibili}"}

    sep = _rileva_separatore(percorso)

    with open(percorso, encoding="utf-8-sig") as f:
        reader = csv.DictReader(f, delimiter=sep)
        colonne = reader.fieldnames or []
        righe = []
        for i, row in enumerate(reader):
            if limite_righe and i >= limite_righe:
                break
            righe.append(dict(row))

    # Conta righe totali
    with open(percorso, encoding="utf-8-sig") as f:
        totale = sum(1 for _ in f) - 1  # meno header

    return {
        "file": nome_file,
        "colonne": colonne,
        "righe": righe,
        "righe_mostrate": len(righe),
        "righe_totali": totale,
        "separatore": sep,
    }


def modifica_csv(nome_file: str, modifiche: list) -> dict:
    """
    Modifica righe specifiche di un CSV esistente in exports/.

    modifiche: lista di dict, ognuno con:
      - riga: indice riga (0-based, escluso header)
      - colonna: nome della colonna da modificare
      - valore: nuovo valore

    Esempio: [{"riga": 0, "colonna": "descrizione", "valore": "Nuova descrizione"}]
    """
    nome_file = os.path.basename(nome_file)
    percorso = os.path.join(Config.EXPORTS_DIR, nome_file)

    if not os.path.exists(percorso):
        return {"errore": f"File '{nome_file}' non trovato"}

    sep = _rileva_separatore(percorso)

    # Leggi tutto il CSV
    with open(percorso, encoding="utf-8-sig") as f:
        reader = csv.DictReader(f, delimiter=sep)
        colonne = reader.fieldnames or []
        righe = [dict(row) for row in reader]

    # Controlla se servono colonne nuove
    nuove_colonne = set()
    for m in modifiche:
        col = m.get("colonna", "")
        if col and col not in colonne:
            nuove_colonne.add(col)
    if nuove_colonne:
        colonne = colonne + sorted(nuove_colonne)

    # Applica modifiche
    modificate = 0
    errori = []
    for m in modifiche:
        idx = m.get("riga")
        col = m.get("colonna", "")
        val = m.get("valore", "")

        if idx is None or not col:
            errori.append(f"Modifica invalida: {m}")
            continue

        if idx < 0 or idx >= len(righe):
            errori.append(f"Riga {idx} fuori range (0-{len(righe)-1})")
            continue

        righe[idx][col] = val
        modificate += 1

    # Riscrivi il CSV
    with open(percorso, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=colonne, delimiter=sep, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(righe)

    return {
        "successo": True,
        "file": nome_file,
        "modifiche_applicate": modificate,
        "errori": errori if errori else None,
        "righe_totali": len(righe),
        "colonne": colonne,
    }


def aggiungi_colonna_csv(nome_file: str, nome_colonna: str, valore_default: str = "") -> dict:
    """
    Aggiunge una nuova colonna a un CSV esistente.
    Utile per aggiungere colonne OEM o altre info mancanti.
    """
    nome_file = os.path.basename(nome_file)
    percorso = os.path.join(Config.EXPORTS_DIR, nome_file)

    if not os.path.exists(percorso):
        return {"errore": f"File '{nome_file}' non trovato"}

    sep = _rileva_separatore(percorso)

    with open(percorso, encoding="utf-8-sig") as f:
        reader = csv.DictReader(f, delimiter=sep)
        colonne = reader.fieldnames or []
        righe = [dict(row) for row in reader]

    if nome_colonna in colonne:
        return {"errore": f"Colonna '{nome_colonna}' esiste già"}

    colonne.append(nome_colonna)
    for riga in righe:
        riga[nome_colonna] = valore_default

    with open(percorso, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=colonne, delimiter=sep, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(righe)

    return {
        "successo": True,
        "file": nome_file,
        "colonna_aggiunta": nome_colonna,
        "righe_aggiornate": len(righe),
    }


def modifica_csv_bulk(nome_file: str, colonna: str, valore: str, filtro_colonna: str = None, filtro_valore: str = None) -> dict:
    """
    Modifica una colonna su TUTTE le righe (o solo quelle che matchano un filtro).

    Esempio: modifica_csv_bulk("r304.csv", "oem", "11427566327")
    → mette "11427566327" nella colonna "oem" di tutte le righe

    Con filtro: modifica_csv_bulk("r304.csv", "oem", "11427566327", "marca", "MANN")
    → solo sulle righe dove marca == "MANN"
    """
    nome_file = os.path.basename(nome_file)
    percorso = os.path.join(Config.EXPORTS_DIR, nome_file)

    if not os.path.exists(percorso):
        return {"errore": f"File '{nome_file}' non trovato"}

    sep = _rileva_separatore(percorso)

    with open(percorso, encoding="utf-8-sig") as f:
        reader = csv.DictReader(f, delimiter=sep)
        colonne = reader.fieldnames or []
        righe = [dict(row) for row in reader]

    # Aggiungi colonna se non esiste
    if colonna not in colonne:
        colonne.append(colonna)

    modificate = 0
    for riga in righe:
        if filtro_colonna and filtro_valore:
            if riga.get(filtro_colonna, "").strip().lower() != filtro_valore.strip().lower():
                continue
        riga[colonna] = valore
        modificate += 1

    with open(percorso, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=colonne, delimiter=sep, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(righe)

    return {
        "successo": True,
        "file": nome_file,
        "colonna": colonna,
        "righe_modificate": modificate,
        "righe_totali": len(righe),
    }
