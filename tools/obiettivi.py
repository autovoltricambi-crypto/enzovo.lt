"""Gestione obiettivi e task — sistema ADHD-friendly con scadenze e priorità."""
import json
import os
import uuid
from datetime import datetime, date
from config import Config

OBIETTIVI_PATH = os.path.join(Config.DATA_DIR, "obiettivi.json")


def _carica() -> dict:
    if not os.path.exists(OBIETTIVI_PATH):
        return {"obiettivi": []}
    with open(OBIETTIVI_PATH, encoding="utf-8") as f:
        return json.load(f)


def _salva(data: dict):
    os.makedirs(os.path.dirname(OBIETTIVI_PATH), exist_ok=True)
    with open(OBIETTIVI_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def _giorni_rimanenti(scadenza: str | None) -> int | None:
    if not scadenza:
        return None
    try:
        delta = date.fromisoformat(scadenza) - date.today()
        return delta.days
    except Exception:
        return None


def crea_obiettivo(
    titolo: str,
    descrizione: str,
    scadenza: str | None = None,
    priorita: str = "media",
) -> dict:
    """
    Crea un nuovo obiettivo principale.
    priorita: 'alta' | 'media' | 'bassa'
    scadenza: formato YYYY-MM-DD (es. '2026-04-30')
    """
    data = _carica()
    obiettivo = {
        "id": str(uuid.uuid4())[:8],
        "titolo": titolo,
        "descrizione": descrizione,
        "scadenza": scadenza,
        "priorita": priorita,
        "stato": "in_corso",
        "creato": datetime.now().isoformat(),
        "task": [],
    }
    data["obiettivi"].append(obiettivo)
    _salva(data)
    return {"successo": True, "obiettivo": obiettivo}


def aggiungi_task(
    obiettivo_id: str,
    titolo: str,
    scadenza: str | None = None,
    priorita: str = "media",
    note: str = "",
) -> dict:
    """
    Aggiunge un task a un obiettivo esistente.
    obiettivo_id: ID dell'obiettivo (8 caratteri)
    """
    data = _carica()
    for ob in data["obiettivi"]:
        if ob["id"] == obiettivo_id:
            task = {
                "id": str(uuid.uuid4())[:8],
                "titolo": titolo,
                "stato": "da_fare",
                "priorita": priorita,
                "scadenza": scadenza,
                "note": note,
                "creato": datetime.now().isoformat(),
                "completato": None,
            }
            ob["task"].append(task)
            _salva(data)
            return {"successo": True, "task": task, "obiettivo_id": obiettivo_id}
    return {"errore": f"Obiettivo '{obiettivo_id}' non trovato"}


def completa_task(task_id: str) -> dict:
    """Segna un task come completato."""
    data = _carica()
    for ob in data["obiettivi"]:
        for task in ob["task"]:
            if task["id"] == task_id:
                task["stato"] = "completato"
                task["completato"] = datetime.now().isoformat()
                # Se tutti i task sono completati, completa l'obiettivo
                if all(t["stato"] == "completato" for t in ob["task"]):
                    ob["stato"] = "completato"
                _salva(data)
                return {"successo": True, "task_id": task_id, "obiettivo": ob["titolo"]}
    return {"errore": f"Task '{task_id}' non trovato"}


def aggiorna_task(
    task_id: str,
    stato: str | None = None,
    note: str | None = None,
    priorita: str | None = None,
    scadenza: str | None = None,
) -> dict:
    """
    Aggiorna un task esistente.
    stato: 'da_fare' | 'in_corso' | 'completato' | 'bloccato'
    """
    data = _carica()
    for ob in data["obiettivi"]:
        for task in ob["task"]:
            if task["id"] == task_id:
                if stato:
                    task["stato"] = stato
                    if stato == "completato":
                        task["completato"] = datetime.now().isoformat()
                if note is not None:
                    task["note"] = note
                if priorita:
                    task["priorita"] = priorita
                if scadenza:
                    task["scadenza"] = scadenza
                _salva(data)
                return {"successo": True, "task": task}
    return {"errore": f"Task '{task_id}' non trovato"}


def completa_obiettivo(obiettivo_id: str) -> dict:
    """Segna un obiettivo come completato."""
    data = _carica()
    for ob in data["obiettivi"]:
        if ob["id"] == obiettivo_id:
            ob["stato"] = "completato"
            _salva(data)
            return {"successo": True, "obiettivo": ob["titolo"]}
    return {"errore": f"Obiettivo '{obiettivo_id}' non trovato"}


def lista_obiettivi(solo_attivi: bool = True) -> dict:
    """
    Ritorna tutti gli obiettivi con i loro task.
    solo_attivi: se True, esclude gli obiettivi completati
    """
    data = _carica()
    obiettivi = data["obiettivi"]
    if solo_attivi:
        obiettivi = [o for o in obiettivi if o["stato"] != "completato"]

    # Aggiunge giorni rimanenti a ogni obiettivo e task
    for ob in obiettivi:
        ob["giorni_rimanenti"] = _giorni_rimanenti(ob.get("scadenza"))
        for task in ob["task"]:
            task["giorni_rimanenti"] = _giorni_rimanenti(task.get("scadenza"))

    return {"obiettivi": obiettivi, "totale": len(obiettivi)}


def priorita_oggi() -> dict:
    """
    Analizza obiettivi e task e suggerisce cosa fare oggi.
    Logica ADHD-friendly: max 3 task, ordinati per urgenza e priorità.
    """
    data = _carica()
    candidati = []

    for ob in data["obiettivi"]:
        if ob["stato"] == "completato":
            continue
        for task in ob["task"]:
            if task["stato"] in ("da_fare", "in_corso", "bloccato"):
                giorni = _giorni_rimanenti(task.get("scadenza")) or _giorni_rimanenti(ob.get("scadenza"))
                punteggio = 0
                # Urgenza scadenza
                if giorni is not None:
                    if giorni <= 1:
                        punteggio += 100
                    elif giorni <= 3:
                        punteggio += 50
                    elif giorni <= 7:
                        punteggio += 20
                # Priorità
                if task["priorita"] == "alta":
                    punteggio += 30
                elif task["priorita"] == "media":
                    punteggio += 10
                # In corso ha precedenza
                if task["stato"] == "in_corso":
                    punteggio += 40

                candidati.append({
                    "task_id": task["id"],
                    "task": task["titolo"],
                    "obiettivo": ob["titolo"],
                    "obiettivo_id": ob["id"],
                    "stato": task["stato"],
                    "priorita": task["priorita"],
                    "giorni_rimanenti": giorni,
                    "note": task.get("note", ""),
                    "punteggio": punteggio,
                })

    candidati.sort(key=lambda x: x["punteggio"], reverse=True)
    top3 = candidati[:3]

    if not top3:
        return {"messaggio": "Nessun task in sospeso. Tutti gli obiettivi sono completati!", "task_oggi": []}

    return {
        "task_oggi": top3,
        "messaggio": f"Hai {len(candidati)} task in sospeso. Ecco i 3 più urgenti per oggi:",
    }


def statistiche_obiettivi() -> dict:
    """Ritorna statistiche generali sugli obiettivi."""
    data = _carica()
    totale = len(data["obiettivi"])
    completati = sum(1 for o in data["obiettivi"] if o["stato"] == "completato")
    in_corso = totale - completati

    task_totali = sum(len(o["task"]) for o in data["obiettivi"])
    task_completati = sum(
        sum(1 for t in o["task"] if t["stato"] == "completato")
        for o in data["obiettivi"]
    )

    return {
        "obiettivi": {"totale": totale, "in_corso": in_corso, "completati": completati},
        "task": {"totale": task_totali, "completati": task_completati, "in_sospeso": task_totali - task_completati},
    }
