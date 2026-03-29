import json
import asyncio
import logging
from anthropic import AsyncAnthropic

logger = logging.getLogger(__name__)

from config import Config
from tools.obiettivi import (
    crea_obiettivo,
    aggiungi_task,
    completa_task,
    aggiorna_task,
    completa_obiettivo,
    lista_obiettivi,
    priorita_oggi,
    priorita_periodo,
    statistiche_obiettivi,
    stato_gamification,
)
from tools.wordpress_write import (
    crea_prodotto,
    modifica_prodotto,
    crea_pagina_html,
    scrivi_pagina_html,
    leggi_pagina_html,
    lista_prodotti,
    ispeziona_pagina_elementor,
    lista_pagine_elementor,
    importa_prodotti_bulk,
    crea_struttura_categorie,
    aggiungi_attributi_prodotto,
)
from tools.cataloghi import cerca_tutti_cataloghi, cerca_catalogo, naviga_web, accedi_portale_b2b
from tools.prezzi import calcola_prezzo_vendita, scorporo_iva
from tools.csv_export import esporta_csv, lista_csv_salvati
from tools.memoria import (
    salva_ricerca,
    cerca_in_memoria,
    salva_nota,
    aggiorna_contesto_sito,
    leggi_contesto_sito,
    carica_contesto_agente,
    carica_conoscenze,
    lista_knowledge,
    leggi_knowledge,
    aggiorna_knowledge,
    crea_knowledge,
)

Config.validate()

client = AsyncAnthropic(api_key=Config.ANTHROPIC_API_KEY)

# ==========================================
# DEFINIZIONE TOOL PER CLAUDE
# ==========================================

TOOLS = [
    # --- WordPress / WooCommerce ---
    {
        "name": "crea_prodotto",
        "description": "Crea un nuovo prodotto WooCommerce nel sito.",
        "input_schema": {
            "type": "object",
            "properties": {
                "nome": {"type": "string", "description": "Nome del prodotto"},
                "prezzo": {"type": "number", "description": "Prezzo di listino"},
                "descrizione": {"type": "string", "description": "Descrizione dettagliata"},
                "sku": {"type": "string", "description": "Codice SKU unico"},
                "stock": {"type": "integer", "description": "Quantità in stock (default: 0)"},
                "categoria": {"type": "string", "description": "Nome categoria (es: 'Filtri Olio')"},
                "related_sku_code": {"type": "string", "description": "Codice interno cross-reference per il plugin compatibilità veicoli (es: R304, OP400, A2181). Diverso dallo SKU — raggruppa lo stesso ricambio di marche diverse. OBBLIGATORIO per prodotti non universali."},
            },
            "required": ["nome", "prezzo", "descrizione", "sku"],
        },
    },
    {
        "name": "modifica_prodotto",
        "description": "Modifica un prodotto WooCommerce esistente.",
        "input_schema": {
            "type": "object",
            "properties": {
                "product_id": {"type": "integer", "description": "ID del prodotto"},
                "nome": {"type": "string"},
                "prezzo": {"type": "number"},
                "descrizione": {"type": "string"},
                "stock": {"type": "integer"},
            },
            "required": ["product_id"],
        },
    },
    {
        "name": "importa_prodotti_bulk",
        "description": (
            "Importa una lista di prodotti in WooCommerce in una sola chiamata (batch da 5 in parallelo). "
            "Usa questo invece di chiamare crea_prodotto N volte. "
            "Ogni prodotto deve avere: nome, prezzo, descrizione, sku. "
            "Opzionali: stock, categoria, attributi (dict con marca_auto/modello/anno/codice_oe)."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "prodotti": {
                    "type": "array",
                    "description": "Lista di prodotti da importare",
                    "items": {
                        "type": "object",
                        "properties": {
                            "nome": {"type": "string"},
                            "prezzo": {"type": "number"},
                            "descrizione": {"type": "string"},
                            "sku": {"type": "string"},
                            "stock": {"type": "integer"},
                            "categoria": {"type": "string"},
                            "attributi": {"type": "object"},
                            "related_sku_code": {"type": "string", "description": "Codice interno cross-reference (es: R304, OP400, A2181). OBBLIGATORIO per prodotti non universali."},
                        },
                        "required": ["nome", "prezzo", "descrizione", "sku"],
                    },
                }
            },
            "required": ["prodotti"],
        },
    },
    {
        "name": "crea_struttura_categorie",
        "description": (
            "Crea un albero di categorie WooCommerce rispettando la gerarchia. "
            "Usa per impostare la struttura del sito simile ad AutoDoc."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "categorie": {
                    "type": "array",
                    "description": "Lista categorie con nome e parent opzionale",
                    "items": {
                        "type": "object",
                        "properties": {
                            "nome": {"type": "string"},
                            "parent": {"type": "string", "description": "Nome categoria parent (null se radice)"},
                        },
                        "required": ["nome"],
                    },
                }
            },
            "required": ["categorie"],
        },
    },
    {
        "name": "aggiungi_attributi_prodotto",
        "description": "Aggiunge attributi a un prodotto (compatibilità veicolo, codice OE, marca auto, ecc.).",
        "input_schema": {
            "type": "object",
            "properties": {
                "product_id": {"type": "integer", "description": "ID prodotto"},
                "attributi": {
                    "type": "object",
                    "description": "Dict con attributi es: {\"marca_auto\": \"BMW\", \"modello\": \"Serie 3\", \"codice_oe\": \"11427566327\"}",
                },
            },
            "required": ["product_id", "attributi"],
        },
    },
    {
        "name": "lista_prodotti",
        "description": "Elenca prodotti WooCommerce con filtri opzionali.",
        "input_schema": {
            "type": "object",
            "properties": {
                "search": {"type": "string"},
                "categoria": {"type": "string"},
                "limit": {"type": "integer", "description": "Max risultati (default 100)"},
            },
        },
    },
    {
        "name": "crea_pagina_html",
        "description": "Crea una nuova pagina HTML nel sito WordPress.",
        "input_schema": {
            "type": "object",
            "properties": {
                "titolo": {"type": "string"},
                "contenuto_html": {"type": "string"},
                "slug": {"type": "string"},
                "stato": {"type": "string", "enum": ["draft", "publish"]},
            },
            "required": ["titolo", "contenuto_html"],
        },
    },
    {
        "name": "scrivi_pagina_html",
        "description": "Modifica il contenuto HTML di una pagina WordPress esistente.",
        "input_schema": {
            "type": "object",
            "properties": {
                "page_id": {"type": "integer"},
                "contenuto_html": {"type": "string"},
                "titolo": {"type": "string"},
                "stato": {"type": "string", "enum": ["draft", "publish"]},
            },
            "required": ["page_id", "contenuto_html"],
        },
    },
    {
        "name": "leggi_pagina_html",
        "description": "Legge il contenuto HTML di una pagina WordPress.",
        "input_schema": {
            "type": "object",
            "properties": {"page_id": {"type": "integer"}},
            "required": ["page_id"],
        },
    },
    {
        "name": "lista_pagine_elementor",
        "description": "Lista tutte le pagine del sito, distinguendo Elementor da HTML puro.",
        "input_schema": {"type": "object", "properties": {}},
    },
    {
        "name": "ispeziona_pagina_elementor",
        "description": "Legge i metadati Elementor di una pagina specifica.",
        "input_schema": {
            "type": "object",
            "properties": {"page_id": {"type": "integer"}},
            "required": ["page_id"],
        },
    },
    # --- Navigazione Web ---
    {
        "name": "naviga_web",
        "description": (
            "Naviga qualsiasi sito web con un browser reale e completa l'obiettivo specificato. "
            "Usa per: analizzare AutoDoc e altri competitor, estrarre strutture/categorie/prezzi, "
            "leggere pagine di fornitori, raccogliere dati da qualsiasi sito. "
            "Non limitato ai cataloghi B2B — funziona su qualsiasi URL."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "url": {"type": "string", "description": "URL del sito da visitare"},
                "obiettivo": {
                    "type": "string",
                    "description": "Cosa fare/estrarre. Es: 'Elenca le categorie principali', 'Trova prezzi filtri olio BMW'",
                },
            },
            "required": ["url", "obiettivo"],
        },
    },
    # --- Portali B2B autenticati ---
    {
        "name": "accedi_portale_b2b",
        "description": (
            "Accede a un portale B2B usando le credenziali salvate nel .env (NON le chiede all'utente) "
            "e completa l'obiettivo specificato. "
            "Usalo per: AZ Car B2B, Elring, Corteco, Valeo, AutoDoc o qualsiasi portale configurato. "
            "Es: portale='azcar', obiettivo='cerca filtri olio BMW e dammi prezzi e codici'"
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "portale": {
                    "type": "string",
                    "description": "Chiave portale: 'azcar', 'elring', 'corteco', 'valeo', 'autodoc'",
                },
                "obiettivo": {
                    "type": "string",
                    "description": "Cosa fare dopo il login (es: 'cerca filtri olio BMW Serie 3 con prezzi')",
                },
            },
            "required": ["portale", "obiettivo"],
        },
    },
    # --- Cataloghi B2B (navigazione pubblica) ---
    {
        "name": "cerca_tutti_cataloghi",
        "description": "Cerca un prodotto su TUTTI i cataloghi B2B (Elring, Corteco, Valeo, AutoDoc) in parallelo.",
        "input_schema": {
            "type": "object",
            "properties": {"query": {"type": "string", "description": "Prodotto da cercare"}},
            "required": ["query"],
        },
    },
    {
        "name": "cerca_catalogo",
        "description": "Cerca un prodotto su un catalogo B2B specifico.",
        "input_schema": {
            "type": "object",
            "properties": {
                "catalogo": {"type": "string", "enum": ["Elring", "Corteco", "Valeo", "AutoDoc"]},
                "query": {"type": "string"},
            },
            "required": ["catalogo", "query"],
        },
    },
    # --- Prezzi ---
    {
        "name": "calcola_prezzo_vendita",
        "description": "Calcola prezzo di vendita da costo fornitore (margine + IVA).",
        "input_schema": {
            "type": "object",
            "properties": {
                "costo": {"type": "number"},
                "margine": {"type": "number", "description": "Margine % (default dal contesto o 30%)"},
                "iva": {"type": "number", "description": "IVA % (default 22%)"},
            },
            "required": ["costo"],
        },
    },
    {
        "name": "scorporo_iva",
        "description": "Estrae il prezzo netto da un prezzo IVA inclusa.",
        "input_schema": {
            "type": "object",
            "properties": {
                "prezzo_ivato": {"type": "number"},
                "iva": {"type": "number", "description": "IVA % (default 22%)"},
            },
            "required": ["prezzo_ivato"],
        },
    },
    # --- Export ---
    {
        "name": "esporta_csv",
        "description": (
            "Esporta lista prodotti/dati in CSV scaricabile (separatore ; per Excel italiano). "
            "Aggiungi sempre una descrizione chiara (es. 'Compatibilità veicoli R304 - BMW N47') "
            "così il file è ritrovabile in seguito."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "prodotti": {
                    "type": "array",
                    "items": {"type": "object"},
                    "description": "Lista di prodotti/dati da esportare",
                },
                "nome_file": {"type": "string", "description": "Nome file CSV (senza estensione)"},
                "descrizione": {"type": "string", "description": "Descrizione del contenuto (es. 'Compatibilità veicoli R304')"},
            },
            "required": ["prodotti"],
        },
    },
    {
        "name": "lista_csv_salvati",
        "description": (
            "Ritorna l'elenco di tutti i CSV salvati con nome, descrizione e data. "
            "Usalo quando l'utente vuole trovare un CSV precedentemente esportato, "
            "ad esempio un file compatibilità veicoli."
        ),
        "input_schema": {"type": "object", "properties": {}},
    },
    # --- Memoria e Contesto ---
    {
        "name": "aggiorna_contesto_sito",
        "description": (
            "Salva una decisione, preferenza o stato del sito in memoria permanente. "
            "Persiste tra sessioni — usalo per ricordare decisioni importanti. "
            "Es: margine_default, struttura_categorie, preferenze_utente, ultimo_import."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "chiave": {"type": "string", "description": "Nome della voce da salvare (es: 'margine_default')"},
                "valore": {"type": "string", "description": "Valore da ricordare"},
            },
            "required": ["chiave", "valore"],
        },
    },
    {
        "name": "leggi_contesto_sito",
        "description": "Legge il contesto permanente del sito (decisioni passate, preferenze, stato).",
        "input_schema": {
            "type": "object",
            "properties": {
                "chiave": {"type": "string", "description": "Chiave specifica da leggere (ometti per leggere tutto)"},
            },
        },
    },
    {
        "name": "salva_ricerca",
        "description": "Salva una ricerca nella memoria storica.",
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {"type": "string"},
                "catalogo": {"type": "string"},
                "risultati_trovati": {"type": "integer"},
            },
            "required": ["query", "catalogo", "risultati_trovati"],
        },
    },
    {
        "name": "cerca_in_memoria",
        "description": "Cerca nelle ricerche, prodotti o note salvate. Evita di ripetere ricerche già fatte.",
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {"type": "string"},
                "tipo": {"type": "string", "enum": ["ricerche", "prodotti", "note"]},
            },
            "required": ["query"],
        },
    },
    {
        "name": "leggi_knowledge",
        "description": (
            "Legge un file di knowledge base da data/know/. "
            "Usa questo tool quando hai bisogno di expertise specifica su un argomento. "
            "Prima chiama lista_knowledge per vedere i file disponibili, poi leggi quello che ti serve. "
            "I file possono essere su qualsiasi argomento: ricambi, SEO, ads, codice, ecc."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "nome_file": {
                    "type": "string",
                    "description": "Nome del file da leggere (es: 'ricambi.md', 'seo.md'). Ometti per vedere tutti i file disponibili.",
                },
            },
        },
    },
    {
        "name": "aggiorna_knowledge",
        "description": (
            "Sovrascrive un file di knowledge esistente in data/know/ con un nuovo contenuto. "
            "Usalo quando l'utente ti segnala che un'informazione in un know file è errata o da aggiornare. "
            "Prima leggi il file con leggi_knowledge, poi apporta le correzioni e riscrivi il contenuto completo."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "nome_file": {"type": "string", "description": "Nome del file da aggiornare (es: 'seo-ricambi-auto.md')"},
                "contenuto": {"type": "string", "description": "Nuovo contenuto completo del file in formato Markdown"},
            },
            "required": ["nome_file", "contenuto"],
        },
    },
    {
        "name": "crea_knowledge",
        "description": (
            "Crea un nuovo file di knowledge in data/know/. "
            "Usalo quando l'utente chiede di aggiungere un nuovo argomento alla knowledge base, "
            "o quando scopri che manca documentazione utile per un'area specifica."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "nome_file": {"type": "string", "description": "Nome del nuovo file (es: 'nuovo-argomento.md')"},
                "contenuto": {"type": "string", "description": "Contenuto del file in formato Markdown"},
            },
            "required": ["nome_file", "contenuto"],
        },
    },
    {
        "name": "salva_nota",
        "description": "Salva una nota per riferimento futuro.",
        "input_schema": {
            "type": "object",
            "properties": {
                "titolo": {"type": "string"},
                "contenuto": {"type": "string"},
            },
            "required": ["titolo", "contenuto"],
        },
    },
    # ==========================================
    # OBIETTIVI & TASK MANAGER
    # ==========================================
    {
        "name": "crea_obiettivo",
        "description": (
            "Crea un nuovo obiettivo principale con scadenza e priorità. "
            "Usalo quando l'utente vuole raggiungere qualcosa di specifico entro una data. "
            "Dopo aver creato l'obiettivo, scomponilo subito in task concreti con aggiungi_task."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "titolo": {"type": "string", "description": "Titolo breve dell'obiettivo"},
                "descrizione": {"type": "string", "description": "Descrizione dettagliata di cosa si vuole ottenere"},
                "scadenza": {"type": "string", "description": "Data scadenza formato YYYY-MM-DD (es. 2026-04-30)"},
                "priorita": {"type": "string", "enum": ["alta", "media", "bassa"], "description": "Priorità dell'obiettivo"},
            },
            "required": ["titolo", "descrizione"],
        },
    },
    {
        "name": "aggiungi_task",
        "description": (
            "Aggiunge un task concreto e azionabile a un obiettivo. "
            "I task devono essere specifici e realizzabili (es. 'Testare browser-use su Mac', non 'Lavorare sul sito'). "
            "Assegna sempre una priorità e una scadenza realistica."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "obiettivo_id": {"type": "string", "description": "ID dell'obiettivo (8 caratteri)"},
                "titolo": {"type": "string", "description": "Descrizione chiara e azionabile del task"},
                "scadenza": {"type": "string", "description": "Data scadenza YYYY-MM-DD"},
                "priorita": {"type": "string", "enum": ["alta", "media", "bassa"]},
                "note": {"type": "string", "description": "Note aggiuntive o contesto"},
            },
            "required": ["obiettivo_id", "titolo"],
        },
    },
    {
        "name": "completa_task",
        "description": "Segna un task come completato. Usalo appena l'utente o l'agente porta a termine un task.",
        "input_schema": {
            "type": "object",
            "properties": {
                "task_id": {"type": "string", "description": "ID del task (8 caratteri)"},
            },
            "required": ["task_id"],
        },
    },
    {
        "name": "aggiorna_task",
        "description": "Aggiorna stato, note, priorità o scadenza di un task esistente.",
        "input_schema": {
            "type": "object",
            "properties": {
                "task_id": {"type": "string", "description": "ID del task"},
                "stato": {"type": "string", "enum": ["da_fare", "in_corso", "completato", "bloccato"]},
                "note": {"type": "string"},
                "priorita": {"type": "string", "enum": ["alta", "media", "bassa"]},
                "scadenza": {"type": "string", "description": "YYYY-MM-DD"},
            },
            "required": ["task_id"],
        },
    },
    {
        "name": "completa_obiettivo",
        "description": "Segna un obiettivo intero come completato.",
        "input_schema": {
            "type": "object",
            "properties": {
                "obiettivo_id": {"type": "string"},
            },
            "required": ["obiettivo_id"],
        },
    },
    {
        "name": "lista_obiettivi",
        "description": (
            "Ritorna tutti gli obiettivi con i loro task, stato e giorni rimanenti. "
            "Usalo per avere una visione completa di cosa c'è da fare."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "solo_attivi": {"type": "boolean", "description": "Se true (default), esclude gli obiettivi completati"},
            },
        },
    },
    {
        "name": "priorita_oggi",
        "description": "Suggerisce i 3 task più urgenti da fare oggi.",
        "input_schema": {"type": "object", "properties": {}},
    },
    {
        "name": "priorita_periodo",
        "description": (
            "Analizza obiettivi e task e suggerisce le 3 priorità del periodo scelto. "
            "Usalo per pianificare la settimana o il mese. "
            "Tutto il lavoro deve ruotare attorno agli obiettivi principali del periodo. "
            "Usalo quando l'utente chiede 'cosa devo fare questa settimana?' o 'su cosa mi concentro questo mese?'"
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "periodo": {"type": "string", "enum": ["oggi", "settimana", "mese"], "description": "Periodo di pianificazione"},
            },
        },
    },
    {
        "name": "statistiche_obiettivi",
        "description": "Ritorna un riepilogo del progresso: quanti obiettivi e task completati vs in sospeso.",
        "input_schema": {"type": "object", "properties": {}},
    },
    {
        "name": "stato_gamification",
        "description": (
            "Ritorna punteggio XP, streak giorni, achievement sbloccati e prossimo achievement. "
            "Usalo per motivare l'utente: 'Sei a 240 XP, ancora 60 e sblocchi Primo Centinaio!' "
            "Usalo all'inizio sessione e quando un task viene completato."
        ),
        "input_schema": {"type": "object", "properties": {}},
    },
]


# ==========================================
# ESECUZIONE TOOL
# ==========================================

async def esegui_tool(name: str, input_dict: dict) -> dict:
    """Esegue un tool con timeout di 60 secondi."""
    try:
        coro = _dispatch_tool(name, input_dict)
        return await asyncio.wait_for(coro, timeout=60)
    except asyncio.TimeoutError:
        return {"errore": f"Tool '{name}' ha superato il timeout di 60 secondi"}
    except BaseException as e:
        return {"errore": f"Errore esecuzione {name}: {str(e)}"}


async def _dispatch_tool(name: str, input_dict: dict) -> dict:
    """Router tool → funzione."""
    if name == "crea_prodotto":
        return await crea_prodotto(**input_dict)
    elif name == "modifica_prodotto":
        return await modifica_prodotto(**input_dict)
    elif name == "importa_prodotti_bulk":
        return await importa_prodotti_bulk(**input_dict)
    elif name == "crea_struttura_categorie":
        return await crea_struttura_categorie(**input_dict)
    elif name == "aggiungi_attributi_prodotto":
        return await aggiungi_attributi_prodotto(**input_dict)
    elif name == "crea_pagina_html":
        return await crea_pagina_html(**input_dict)
    elif name == "scrivi_pagina_html":
        return await scrivi_pagina_html(**input_dict)
    elif name == "leggi_pagina_html":
        return await leggi_pagina_html(**input_dict)
    elif name == "lista_prodotti":
        return await lista_prodotti(**input_dict)
    elif name == "ispeziona_pagina_elementor":
        return await ispeziona_pagina_elementor(**input_dict)
    elif name == "lista_pagine_elementor":
        return await lista_pagine_elementor()
    elif name == "accedi_portale_b2b":
        return await accedi_portale_b2b(**input_dict)
    elif name == "naviga_web":
        return await naviga_web(**input_dict)
    elif name == "cerca_tutti_cataloghi":
        return await cerca_tutti_cataloghi(**input_dict)
    elif name == "cerca_catalogo":
        return await cerca_catalogo(**input_dict)
    elif name == "calcola_prezzo_vendita":
        return calcola_prezzo_vendita(**input_dict)
    elif name == "scorporo_iva":
        return scorporo_iva(**input_dict)
    elif name == "esporta_csv":
        return esporta_csv(**input_dict)
    elif name == "lista_csv_salvati":
        return lista_csv_salvati()
    elif name == "leggi_knowledge":
        return leggi_knowledge(**input_dict)
    elif name == "aggiorna_knowledge":
        return aggiorna_knowledge(**input_dict)
    elif name == "crea_knowledge":
        return crea_knowledge(**input_dict)
    elif name == "aggiorna_contesto_sito":
        return aggiorna_contesto_sito(**input_dict)
    elif name == "leggi_contesto_sito":
        return leggi_contesto_sito(**input_dict)
    elif name == "salva_ricerca":
        return salva_ricerca(**input_dict)
    elif name == "cerca_in_memoria":
        return cerca_in_memoria(**input_dict)
    elif name == "salva_nota":
        return salva_nota(**input_dict)
    elif name == "crea_obiettivo":
        return crea_obiettivo(**input_dict)
    elif name == "aggiungi_task":
        return aggiungi_task(**input_dict)
    elif name == "completa_task":
        return completa_task(**input_dict)
    elif name == "aggiorna_task":
        return aggiorna_task(**input_dict)
    elif name == "completa_obiettivo":
        return completa_obiettivo(**input_dict)
    elif name == "lista_obiettivi":
        return lista_obiettivi(**input_dict)
    elif name == "priorita_oggi":
        return priorita_oggi()
    elif name == "priorita_periodo":
        return priorita_periodo(**input_dict)
    elif name == "statistiche_obiettivi":
        return statistiche_obiettivi()
    elif name == "stato_gamification":
        return stato_gamification()
    else:
        return {"errore": f"Tool sconosciuto: {name}"}


# ==========================================
# LOOP REACT PRINCIPALE
# ==========================================

async def chat(
    messaggio: str,
    cronologia: list = None,
    progress_callback=None,
) -> tuple[str, list]:
    """
    Loop ReAct autonomo con contesto persistente.

    All'avvio carica il contesto del sito dalla memoria e lo inietta nel
    system prompt — l'agente "ricorda" le sessioni precedenti.
    Tool multipli nello stesso turno vengono eseguiti in parallelo.
    """
    if cronologia is None:
        cronologia = []

    # Carica contesto persistente dalla memoria
    contesto = carica_contesto_agente()

    # Carica obiettivi attivi per iniettarli nel system prompt
    from tools.obiettivi import lista_obiettivi, priorita_oggi
    _ob = lista_obiettivi(solo_attivi=True)
    _ob_list = _ob.get("obiettivi", [])
    _ob_str = ""
    if _ob_list:
        righe = []
        for ob in _ob_list:
            giorni = ob.get("giorni_rimanenti")
            scad = f" — {giorni}g alla scadenza" if giorni is not None else ""
            righe.append(f"• [{ob['priorita'].upper()}] {ob['titolo']}{scad}")
            task_aperti = [t for t in ob.get("task", []) if t["stato"] != "completato"]
            for t in task_aperti[:3]:
                righe.append(f"  → {t['titolo']} [{t['stato']}]")
        _ob_str = "\n".join(righe)
    else:
        _ob_str = "Nessun obiettivo salvato — chiedi all'utente a cosa sta puntando."

    # Carica stato gamification
    from tools.obiettivi import stato_gamification as _sg
    _gam = _sg()
    _streak = _gam.get("streak_giorni", 0)
    _xp = _gam.get("punteggio_totale", 0)
    _ach_ultimo = _gam.get("ultimo_achievement")
    _ach_prossimo = _gam.get("prossimo_achievement")
    _gam_str = f"XP totali: {_xp} | Streak: {_streak} giorni"
    if _ach_ultimo:
        _gam_str += f" | Ultimo achievement: {_ach_ultimo['titolo']}"
    if _ach_prossimo:
        _gam_str += f" | Prossimo: '{_ach_prossimo['titolo']}' (mancano {_ach_prossimo['mancano']} {_ach_prossimo['tipo'].replace('_', ' ')})"

    # Carica knowledge files critici automaticamente
    _know_critico = ""
    for fname in ("azcar-import.md", "plugin-compatibilita.md", "adhd-guida.md", "agente-motivazione.md"):
        r = leggi_knowledge(fname)
        if "contenuto" in r:
            _know_critico += f"\n\n--- {fname} ---\n{r['contenuto']}"

    # Lista di tutti i knowledge file disponibili
    _know_lista = lista_knowledge()
    _know_files = ", ".join(_know_lista.get("files", [])) or "nessuno"

    system_prompt = f"""Sei un agente AI autonomo, esperto e motivato. Puoi fare qualsiasi \
cosa: navigare il web, gestire sistemi, scrivere codice, analizzare dati, risolvere problemi \
tecnici, creare contenuti, fare ricerche approfondite, automatizzare processi e molto altro.

## Identità e modo di operare

Sei un esperto informatico con mentalità da problem solver. Il tuo approccio:

- **Hyper focus** — quando ricevi un task ti concentri completamente su quello, senza \
  distrarti. Non ti fermi finché non è risolto.
- **Autonomia** — tendi a risolvere da solo. Prima di chiedere all'utente, esplora, \
  prova, cerca nei knowledge file, usa i tool. Chiedi solo se hai raggiunto un vero \
  blocco che non puoi superare da solo.
- **Ragionamento attivo** — ti poni domande: "Perché non funziona? Cosa manca? \
  C'è un modo migliore? Ho considerato tutti i casi?". Ragioni ad alta voce sui problemi \
  prima di agire.
- **Orientato alla soluzione** — non ti limiti a descrivere il problema, lo risolvi. \
  Se trovi un ostacolo cerchi un percorso alternativo. Se il primo approccio fallisce, \
  ne provi un secondo senza arrenderti.
- **Adattabile** — non sei limitato a un dominio. Ti adatti al contesto del task: \
  se serve codice scrivi codice, se serve ricerca navighi il web, se serve logica \
  la applichi.
- **Insight proattivi** — mentre lavori, se trovi online o ragioni su qualcosa che \
  potrebbe essere utile per l'utente nel suo specifico contesto (piccola attività, \
  budget limitato, settore ricambi auto), lo segnali esplicitamente. Non aspetti che \
  te lo chieda. Esempio: "Ho trovato questo approccio — nel tuo caso potrebbe funzionare \
  perché...". Se l'insight è rilevante: 1) lo comunichi all'utente contestualizzandolo, \
  2) aggiorni o crei il know file pertinente con aggiorna_knowledge o crea_knowledge, \
  3) salvi la strategia in memoria con salva_nota così non la dimentichi tra sessioni.

Giri localmente sul PC dell'utente (localhost). Il browser che usi tramite naviga_web \
o accedi_portale_b2b si apre fisicamente sul suo schermo — non sei su un server remoto. \
Le credenziali per i portali B2B (AZ Car, ecc.) sono già pre-caricate nel sistema: \
NON chiederle mai all'utente, usa direttamente il tool accedi_portale_b2b.

=== KNOWLEDGE BASE (procedure operative) ==={_know_critico}
==========================================

=== ALTRI KNOWLEDGE DISPONIBILI ===
Usa leggi_knowledge(nome_file) per leggere questi file prima di agire su argomenti correlati:
{_know_files}
====================================

=== GAMIFICATION (sistema ricompensa) ===
{_gam_str}
Usa questi dati per motivare l'utente durante la sessione.
=========================================

=== OBIETTIVI ATTIVI (priorità settimana/mese) ===
{_ob_str}
Tutto il tuo lavoro deve ruotare attorno a questi obiettivi.
Ogni azione che esegui deve avvicinarci a uno di essi.
Se l'utente chiede qualcosa di non collegato, fallo ma ricordagli il focus principale.
==================================================

=== CONTESTO (memoria sessioni precedenti) ===
{contesto}
==============================================

Hai accesso a tool per:
- Navigare e interagire con qualsiasi sito web (naviga_web, accedi_portale_b2b)
- Gestire un sito WordPress/WooCommerce (prodotti, categorie, pagine)
- Cercare su cataloghi B2B e portali fornitore
- Calcolare prezzi, esportare CSV
- Leggere knowledge base di riferimento (leggi_knowledge)
- Salvare memoria e contesto tra sessioni

Quando ricevi un task complesso:
1. ANALIZZA: capisci il problema a fondo — cosa serve esattamente? Cosa potrebbe andare storto?
2. PIANIFICA: descrivi i passi che farai (numerati)
3. ESEGUI: usa i tool, in parallelo dove possibile, senza aspettare conferme per ogni step
4. VERIFICA: controlla il risultato — è quello che ci si aspettava? C'è qualcosa che non torna?
5. MEMORIZZA: salva decisioni importanti con aggiorna_contesto_sito

Per task semplici rispondi direttamente senza pianificazione.
Se qualcosa non funziona, diagnostica prima di cambiare approccio.

=== OBIETTIVI & TASK MANAGER (supporto ADHD) ===

L'utente ha ADHD. Il tuo ruolo non è solo eseguire task tecnici — è anche aiutarlo
a mantenere il focus, ricordargli gli obiettivi e guidarlo passo per passo.

COMPORTAMENTO PROATTIVO:
- **Inizio sessione**: chiama lista_obiettivi() e priorita_periodo("settimana") per capire
  dove siamo. Saluta e ricorda subito l'obiettivo principale della settimana/mese e i task aperti.
  Non chiedere "cosa vuoi fare?" — dì tu cosa c'è da fare in base agli obiettivi.
- **Obiettivo nuovo**: quando l'utente dichiara un obiettivo (es. "voglio aumentare
  le entrate nel negozio"), NON limitarti a salvarlo — ragiona su di esso:
  * Cosa implica concretamente? (es. "negozio locale" → SEO locale, Google My Business,
    più prodotti per coprire più ricerche locali)
  * Scomponilo in 3-5 task specifici e azionabili con scadenze realistiche
  * Chiedi all'utente se manca qualcosa prima di procedere
- **Durante il lavoro**: ricorda all'utente il collegamento tra quello che stai
  facendo e l'obiettivo principale (es. "Sto aggiungendo questi prodotti perché
  coprono ricerche locali per BMW — questo ci avvicina all'obiettivo entrate")
- **Fine sessione o task completato**: celebra il completamento, fai un recap
  breve di cosa è stato fatto e cosa rimane, suggerisci il prossimo passo
- **Se l'utente si perde o cambia argomento**: riportalo gentilmente al focus
  (es. "Possiamo farlo, ma ricorda che l'obiettivo principale oggi è X — vuoi
  finirlo prima?")

REGOLE ADHD:
- Max 3 cose alla volta — mai sovraccaricare
- Task specifici e piccoli (realizzabili in una sessione)
- Celebra ogni completamento, anche piccolo
- Dai sempre un "prossimo passo" chiaro alla fine di ogni risposta
- Se non c'è nessun obiettivo salvato, chiedi all'utente: "A cosa stiamo puntando?
  Dimmi il tuo obiettivo principale così posso aiutarti a organizzarti."
================================================"""

    cronologia.append({"role": "user", "content": messaggio})

    max_iterations = 30
    iteration = 0

    def _content_to_dicts(content_blocks) -> list:
        """Converte ContentBlock SDK objects in dicts serializzabili."""
        result = []
        for block in content_blocks:
            if block.type == "text":
                result.append({"type": "text", "text": block.text})
            elif block.type == "tool_use":
                result.append({
                    "type": "tool_use",
                    "id": block.id,
                    "name": block.name,
                    "input": block.input,
                })
        return result

    while iteration < max_iterations:
        iteration += 1

        # Debug: log stato cronologia prima di ogni chiamata API
        logger.info(f"[CHAT] Iterazione {iteration}, messaggi in cronologia: {len(cronologia)}")
        for i, msg in enumerate(cronologia):
            c = msg.get("content", "")
            if isinstance(c, list):
                types = []
                for b in c:
                    if isinstance(b, dict):
                        types.append(b.get("type", "?"))
                    else:
                        types.append(getattr(b, "type", "?"))
                logger.info(f"  [{i}] {msg['role']}: {types}")
            else:
                logger.info(f"  [{i}] {msg['role']}: text ({len(str(c))} chars)")

        response = await client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=8000,
            system=system_prompt,
            tools=TOOLS,
            messages=cronologia,
        )

        if response.stop_reason == "end_turn":
            risposta_finale = ""
            for block in response.content:
                if hasattr(block, "text"):
                    risposta_finale = block.text
                    break
            cronologia.append({"role": "assistant", "content": risposta_finale})
            return risposta_finale, cronologia

        elif response.stop_reason == "tool_use":
            tool_uses = [b for b in response.content if b.type == "tool_use"]

            # Esegui tool multipli IN PARALLELO
            if progress_callback and len(tool_uses) > 1:
                nomi = ", ".join(t.name for t in tool_uses)
                await progress_callback(f"Esecuzione parallela: {nomi}")

            async def run_tool(tool_use):
                if progress_callback:
                    await progress_callback(f"▶ {tool_use.name}...")
                try:
                    result = await esegui_tool(tool_use.name, tool_use.input)
                    if progress_callback:
                        stato = "✓" if not result.get("errore") else "✗"
                        await progress_callback(f"{stato} {tool_use.name} completato")
                    content = json.dumps(result, ensure_ascii=False)
                    is_error = bool(result.get("errore"))
                except Exception as e:
                    content = json.dumps({"errore": str(e)}, ensure_ascii=False)
                    is_error = True
                    if progress_callback:
                        await progress_callback(f"✗ {tool_use.name} errore: {e}")
                return {
                    "type": "tool_result",
                    "tool_use_id": tool_use.id,
                    "content": content,
                    "is_error": is_error,
                }

            # Raccogli tutti i risultati PRIMA di toccare la cronologia
            try:
                tool_results = await asyncio.gather(*[run_tool(t) for t in tool_uses])
            except Exception as e:
                # gather fallito — crea tool_result di errore per ogni tool
                tool_results = [
                    {
                        "type": "tool_result",
                        "tool_use_id": t.id,
                        "content": json.dumps({"errore": str(e)}, ensure_ascii=False),
                        "is_error": True,
                    }
                    for t in tool_uses
                ]

            # Append ATOMICO — assistant + user insieme, mai separati
            # Converti ContentBlock SDK → dicts puliti per evitare problemi di serializzazione
            cronologia.append({"role": "assistant", "content": _content_to_dicts(response.content)})
            cronologia.append({"role": "user", "content": list(tool_results)})

        elif response.stop_reason == "max_tokens":
            cronologia.append({"role": "assistant", "content": _content_to_dicts(response.content)})
            if progress_callback:
                await progress_callback("Continuo l'elaborazione...")

        else:
            risposta_finale = f"Stop inatteso: {response.stop_reason}"
            cronologia.append({"role": "assistant", "content": risposta_finale})
            return risposta_finale, cronologia

    risposta_finale = "Limite iterazioni raggiunto (30). Task parzialmente completato."
    cronologia.append({"role": "assistant", "content": risposta_finale})
    return risposta_finale, cronologia
