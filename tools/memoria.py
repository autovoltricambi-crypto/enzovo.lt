"""Memoria persistente in JSON per ricerche, prodotti e note."""
import json
import os
from datetime import datetime
from uuid import uuid4
from config import Config


def _carica() -> dict:
    """Carica il file memoria.json, crea struttura vuota se non esiste."""
    if not os.path.exists(Config.MEMORIA_PATH):
        return {
            "ricerche": [],
            "prodotti": [],
            "note": [],
            "contesto_sito": {},
            "clienti_locali": [],
            "preventivi": [],
        }
    memoria = json.load(open(Config.MEMORIA_PATH, encoding="utf-8"))
    # Migrazione: aggiunge contesto_sito se mancante
    if "contesto_sito" not in memoria:
        memoria["contesto_sito"] = {}
    # Migrazione: aggiunge CRM locale se mancante
    if "clienti_locali" not in memoria:
        memoria["clienti_locali"] = []
    if "preventivi" not in memoria:
        memoria["preventivi"] = []
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


def _normalizza_whatsapp(whatsapp: str) -> str:
    """Normalizza il numero WhatsApp mantenendo solo cifre e + iniziale."""
    value = (whatsapp or "").strip().replace(" ", "")
    if not value:
        return ""
    has_plus = value.startswith("+")
    digits = "".join(ch for ch in value if ch.isdigit())
    if not digits:
        return ""
    return f"+{digits}" if has_plus else digits


def _solo_cifre_whatsapp(whatsapp: str) -> str:
    """Ritorna solo le cifre del numero WhatsApp per confronti robusti."""
    return "".join(ch for ch in (whatsapp or "") if ch.isdigit())


def _stesso_whatsapp(a: str, b: str) -> bool:
    """Confronta due numeri WhatsApp ignorando formattazione e +."""
    a_digits = _solo_cifre_whatsapp(a)
    b_digits = _solo_cifre_whatsapp(b)
    return bool(a_digits and b_digits and a_digits == b_digits)


def salva_cliente_locale(
    nome: str,
    whatsapp: str,
    auto: list | None = None,
    acquisti: list | None = None,
    note: str = "",
) -> dict:
    """
    Crea o aggiorna un cliente locale con contatto WhatsApp, veicoli e storico acquisti.
    Se il numero WhatsApp esiste già, aggiorna la scheda esistente.
    """
    memoria = _carica()
    whatsapp_norm = _normalizza_whatsapp(whatsapp)
    if not whatsapp_norm:
        return {"errore": "Numero WhatsApp non valido"}

    auto = [a.strip() for a in (auto or []) if str(a).strip()]
    acquisti = [a for a in (acquisti or []) if a]

    cliente = None
    for c in memoria["clienti_locali"]:
        if _stesso_whatsapp(c.get("whatsapp", ""), whatsapp_norm):
            cliente = c
            break

    now = datetime.now().isoformat()
    if cliente is None:
        cliente = {
            "cliente_id": uuid4().hex[:8],
            "nome": nome.strip(),
            "whatsapp": whatsapp_norm,
            "auto": auto,
            "acquisti": acquisti,
            "note": note.strip(),
            "creato_il": now,
            "aggiornato_il": now,
        }
        memoria["clienti_locali"].append(cliente)
        azione = "creato"
    else:
        if nome.strip():
            cliente["nome"] = nome.strip()
        if note.strip():
            cliente["note"] = note.strip()
        if auto:
            cliente["auto"] = sorted(set((cliente.get("auto") or []) + auto))
        if acquisti:
            cliente["acquisti"] = (cliente.get("acquisti") or []) + acquisti
        cliente["aggiornato_il"] = now
        azione = "aggiornato"

    _salva(memoria)
    return {
        "successo": True,
        "azione": azione,
        "cliente_id": cliente["cliente_id"],
        "whatsapp": cliente["whatsapp"],
    }


def aggiorna_acquisto_cliente(
    whatsapp: str,
    descrizione_acquisto: str,
    auto: str | None = None,
    importo: float | None = None,
) -> dict:
    """Aggiunge uno storico acquisto alla scheda cliente (ricambi venduti localmente)."""
    memoria = _carica()
    whatsapp_norm = _normalizza_whatsapp(whatsapp)
    cliente = next((c for c in memoria["clienti_locali"] if _stesso_whatsapp(c.get("whatsapp", ""), whatsapp_norm)), None)
    if not cliente:
        return {"errore": f"Cliente con WhatsApp '{whatsapp}' non trovato"}

    entry = {
        "data": datetime.now().isoformat(),
        "descrizione": descrizione_acquisto,
    }
    if auto:
        entry["auto"] = auto
        cliente["auto"] = sorted(set((cliente.get("auto") or []) + [auto]))
    if importo is not None:
        entry["importo"] = float(importo)

    cliente["acquisti"] = (cliente.get("acquisti") or []) + [entry]
    cliente["aggiornato_il"] = datetime.now().isoformat()
    _salva(memoria)
    return {"successo": True, "cliente_id": cliente["cliente_id"], "acquisti_totali": len(cliente["acquisti"])}


def registra_preventivo(
    whatsapp: str,
    descrizione: str,
    auto: str | None = None,
    importo: float | None = None,
    stato: str = "inviato",
) -> dict:
    """
    Registra un preventivo cliente.
    Stato consigliato: bozza | inviato | accettato | rifiutato.
    """
    memoria = _carica()
    whatsapp_norm = _normalizza_whatsapp(whatsapp)
    if not whatsapp_norm:
        return {"errore": "Numero WhatsApp non valido"}

    cliente = next((c for c in memoria["clienti_locali"] if _stesso_whatsapp(c.get("whatsapp", ""), whatsapp_norm)), None)
    preventivo = {
        "preventivo_id": uuid4().hex[:10],
        "cliente_id": cliente.get("cliente_id") if cliente else None,
        "whatsapp": whatsapp_norm,
        "auto": auto,
        "descrizione": descrizione,
        "importo": float(importo) if importo is not None else None,
        "stato": stato,
        "data": datetime.now().isoformat(),
    }
    memoria["preventivi"].append(preventivo)
    _salva(memoria)
    return {
        "successo": True,
        "preventivo_id": preventivo["preventivo_id"],
        "cliente_collegato": bool(cliente),
    }


def lista_clienti_locali(query: str | None = None) -> dict:
    """Elenca i clienti locali; query opzionale su nome/numero/auto/acquisti."""
    memoria = _carica()
    clienti = memoria.get("clienti_locali", [])
    if query:
        q = query.lower()
        clienti = [c for c in clienti if q in json.dumps(c, ensure_ascii=False).lower()]
    return {"totale": len(clienti), "clienti": clienti}


def lista_preventivi(stato: str | None = None, whatsapp: str | None = None) -> dict:
    """Elenca preventivi con filtri opzionali per stato e cliente WhatsApp."""
    memoria = _carica()
    preventivi = memoria.get("preventivi", [])
    if stato:
        preventivi = [p for p in preventivi if p.get("stato") == stato]
    if whatsapp:
        whatsapp_norm = _normalizza_whatsapp(whatsapp)
        preventivi = [p for p in preventivi if _stesso_whatsapp(p.get("whatsapp", ""), whatsapp_norm)]
    return {"totale": len(preventivi), "preventivi": preventivi}


def scheda_cliente(whatsapp: str) -> dict:
    """Ritorna la scheda completa cliente con eventuali preventivi associati."""
    memoria = _carica()
    whatsapp_norm = _normalizza_whatsapp(whatsapp)
    cliente = next((c for c in memoria["clienti_locali"] if _stesso_whatsapp(c.get("whatsapp", ""), whatsapp_norm)), None)
    if not cliente:
        return {"trovato": False, "errore": f"Cliente con WhatsApp '{whatsapp}' non trovato"}
    preventivi = [p for p in memoria.get("preventivi", []) if _stesso_whatsapp(p.get("whatsapp", ""), whatsapp_norm)]
    return {"trovato": True, "cliente": cliente, "preventivi": preventivi}


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
        "clienti_locali": len(memoria.get("clienti_locali", [])),
        "preventivi": len(memoria.get("preventivi", [])),
        "file": Config.MEMORIA_PATH,
        "esiste": os.path.exists(Config.MEMORIA_PATH),
    }
