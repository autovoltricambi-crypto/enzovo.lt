"""Gestione obiettivi e task — sistema ADHD-friendly con scadenze e priorità."""
import json
import os
import uuid
from datetime import datetime, date
from config import Config

OBIETTIVI_PATH = os.path.join(Config.DATA_DIR, "obiettivi.json")

ACHIEVEMENTS = [
    {"id": "prima_vittoria", "titolo": "Prima vittoria", "descrizione": "Hai completato il tuo primo task.", "soglia": 1, "tipo": "task_totali"},
    {"id": "momentum", "titolo": "Momentum", "descrizione": "5 task completati.", "soglia": 5, "tipo": "task_totali"},
    {"id": "costruttore", "titolo": "Costruttore", "descrizione": "10 task completati.", "soglia": 10, "tipo": "task_totali"},
    {"id": "macchina", "titolo": "Macchina", "descrizione": "25 task completati.", "soglia": 25, "tipo": "task_totali"},
    {"id": "streak_3", "titolo": "Fuoco!", "descrizione": "3 giorni di fila con almeno un task.", "soglia": 3, "tipo": "streak"},
    {"id": "streak_7", "titolo": "Settimana perfetta", "descrizione": "7 giorni di fila.", "soglia": 7, "tipo": "streak"},
    {"id": "streak_30", "titolo": "Mese di ferro", "descrizione": "30 giorni di fila.", "soglia": 30, "tipo": "streak"},
    {"id": "xp_100", "titolo": "Primo centinaio", "descrizione": "100 XP guadagnati.", "soglia": 100, "tipo": "xp"},
    {"id": "xp_500", "titolo": "500 XP", "descrizione": "500 XP guadagnati.", "soglia": 500, "tipo": "xp"},
    {"id": "xp_1000", "titolo": "Mille punti", "descrizione": "1000 XP guadagnati.", "soglia": 1000, "tipo": "xp"},
]


def _carica() -> dict:
    if not os.path.exists(OBIETTIVI_PATH):
        return {"obiettivi": [], "gamification": _gamification_vuota()}
    data = json.load(open(OBIETTIVI_PATH, encoding="utf-8"))
    if "gamification" not in data:
        data["gamification"] = _gamification_vuota()
    return data


def _gamification_vuota() -> dict:
    return {
        "punteggio_totale": 0,
        "streak_giorni": 0,
        "ultimo_completamento": None,
        "task_totali_completati": 0,
        "achievements": [],
        "ultimo_achievement": None,
    }


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


def _aggiorna_gamification(data: dict, priorita_task: str) -> dict:
    """Aggiorna punteggio, streak e achievement dopo un completamento."""
    g = data["gamification"]
    oggi = date.today().isoformat()

    # Punteggio base
    xp_guadagnati = 10
    if priorita_task == "alta":
        xp_guadagnati += 20
    elif priorita_task == "media":
        xp_guadagnati += 5

    # Streak
    ultimo = g.get("ultimo_completamento")
    if ultimo:
        giorni_passati = (date.today() - date.fromisoformat(ultimo[:10])).days
        if giorni_passati == 0:
            pass  # già completato oggi, streak invariato
        elif giorni_passati == 1:
            g["streak_giorni"] += 1
            xp_guadagnati += 5  # bonus streak
        else:
            g["streak_giorni"] = 1  # streak rotto, riparte
    else:
        g["streak_giorni"] = 1

    g["ultimo_completamento"] = datetime.now().isoformat()
    g["punteggio_totale"] += xp_guadagnati
    g["task_totali_completati"] = g.get("task_totali_completati", 0) + 1

    # Achievement check
    nuovi_achievement = []
    achievement_sbloccati = {a["id"] for a in g.get("achievements", [])}
    for ach in ACHIEVEMENTS:
        if ach["id"] in achievement_sbloccati:
            continue
        sbloccato = False
        if ach["tipo"] == "task_totali" and g["task_totali_completati"] >= ach["soglia"]:
            sbloccato = True
        elif ach["tipo"] == "streak" and g["streak_giorni"] >= ach["soglia"]:
            sbloccato = True
        elif ach["tipo"] == "xp" and g["punteggio_totale"] >= ach["soglia"]:
            sbloccato = True
        if sbloccato:
            entry = {**ach, "sbloccato": datetime.now().isoformat()}
            g["achievements"].append(entry)
            g["ultimo_achievement"] = entry
            nuovi_achievement.append(ach["titolo"])

    return {
        "xp_guadagnati": xp_guadagnati,
        "punteggio_totale": g["punteggio_totale"],
        "streak_giorni": g["streak_giorni"],
        "nuovi_achievement": nuovi_achievement,
    }


def completa_task(task_id: str) -> dict:
    """Segna un task come completato e aggiorna il sistema di ricompensa."""
    data = _carica()
    for ob in data["obiettivi"]:
        for task in ob["task"]:
            if task["id"] == task_id:
                task["stato"] = "completato"
                task["completato"] = datetime.now().isoformat()
                if all(t["stato"] == "completato" for t in ob["task"]):
                    ob["stato"] = "completato"
                gamification = _aggiorna_gamification(data, task.get("priorita", "media"))
                _salva(data)
                return {
                    "successo": True,
                    "task_id": task_id,
                    "obiettivo": ob["titolo"],
                    **gamification,
                }
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


def priorita_periodo(periodo: str = "settimana") -> dict:
    """
    Analizza obiettivi e task e suggerisce le priorità del periodo.
    periodo: 'oggi' | 'settimana' | 'mese'
    Logica ADHD-friendly: max 3 task, tutto ruota attorno agli obiettivi principali.
    """
    data = _carica()
    candidati = []

    giorni_periodo = {"oggi": 1, "settimana": 7, "mese": 30}.get(periodo, 7)

    for ob in data["obiettivi"]:
        if ob["stato"] == "completato":
            continue
        for task in ob["task"]:
            if task["stato"] in ("da_fare", "in_corso", "bloccato"):
                giorni_task = _giorni_rimanenti(task.get("scadenza"))
                giorni_ob = _giorni_rimanenti(ob.get("scadenza"))
                giorni = giorni_task if giorni_task is not None else giorni_ob

                punteggio = 0
                # Urgenza scadenza rispetto al periodo
                if giorni is not None:
                    if giorni <= 1:
                        punteggio += 100
                    elif giorni <= giorni_periodo:
                        punteggio += 70
                    elif giorni <= giorni_periodo * 2:
                        punteggio += 30
                # Priorità obiettivo padre
                if ob["priorita"] == "alta":
                    punteggio += 40
                elif ob["priorita"] == "media":
                    punteggio += 20
                # Priorità task
                if task["priorita"] == "alta":
                    punteggio += 30
                elif task["priorita"] == "media":
                    punteggio += 10
                # In corso ha precedenza
                if task["stato"] == "in_corso":
                    punteggio += 50

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
        return {"messaggio": "Nessun task in sospeso. Tutti gli obiettivi sono completati!", "task_periodo": []}

    label = {"oggi": "oggi", "settimana": "questa settimana", "mese": "questo mese"}.get(periodo, "questo periodo")
    return {
        "task_periodo": top3,
        "periodo": periodo,
        "messaggio": f"Hai {len(candidati)} task in sospeso. Ecco i 3 più importanti per {label}:",
    }


def priorita_oggi() -> dict:
    """Alias per compatibilità — chiama priorita_periodo('oggi')."""
    r = priorita_periodo("oggi")
    # Rinomina task_periodo in task_oggi per compatibilità
    r["task_oggi"] = r.pop("task_periodo", [])
    return r


def stato_gamification() -> dict:
    """Ritorna punteggio, streak, achievement e statistiche gamification."""
    data = _carica()
    g = data.get("gamification", _gamification_vuota())
    return {
        "punteggio_totale": g.get("punteggio_totale", 0),
        "streak_giorni": g.get("streak_giorni", 0),
        "task_totali_completati": g.get("task_totali_completati", 0),
        "ultimo_completamento": g.get("ultimo_completamento"),
        "achievements": g.get("achievements", []),
        "ultimo_achievement": g.get("ultimo_achievement"),
        "prossimo_achievement": _prossimo_achievement(g),
    }


def _prossimo_achievement(g: dict) -> dict | None:
    """Trova il prossimo achievement più vicino da sbloccare."""
    sbloccati = {a["id"] for a in g.get("achievements", [])}
    candidati = []
    for ach in ACHIEVEMENTS:
        if ach["id"] in sbloccati:
            continue
        if ach["tipo"] == "task_totali":
            mancano = ach["soglia"] - g.get("task_totali_completati", 0)
        elif ach["tipo"] == "streak":
            mancano = ach["soglia"] - g.get("streak_giorni", 0)
        elif ach["tipo"] == "xp":
            mancano = ach["soglia"] - g.get("punteggio_totale", 0)
        else:
            continue
        if mancano > 0:
            candidati.append({**ach, "mancano": mancano})
    if not candidati:
        return None
    return min(candidati, key=lambda x: x["mancano"])


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
