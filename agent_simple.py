import json
import asyncio
from anthropic import AsyncAnthropic

from config import Config
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
from tools.csv_export import esporta_csv
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
        "description": "Esporta lista prodotti in CSV scaricabile (separatore ; per Excel italiano).",
        "input_schema": {
            "type": "object",
            "properties": {
                "prodotti": {
                    "type": "array",
                    "items": {"type": "object"},
                    "description": "Lista di prodotti/dati da esportare",
                },
                "nome_file": {"type": "string", "description": "Nome file CSV (senza estensione)"},
            },
            "required": ["prodotti"],
        },
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
    except Exception as e:
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
    elif name == "leggi_knowledge":
        return leggi_knowledge(**input_dict)
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

    system_prompt = f"""Sei un agente AI autonomo e generale. Puoi fare qualsiasi cosa \
l'utente ti chiede: navigare il web, gestire siti, cercare informazioni, scrivere codice, \
analizzare dati, creare contenuti, fare ricerche, e molto altro.

Non sei limitato a un dominio specifico. Adatti le tue capacità al contesto del task.

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
1. PIANIFICA: descrivi i passi che farai (numerati)
2. ESEGUI: usa i tool, in parallelo dove possibile
3. VERIFICA: controlla il risultato
4. MEMORIZZA: salva decisioni importanti con aggiorna_contesto_sito

Per task semplici rispondi direttamente.
Ricorda le preferenze dell'utente e salvale in memoria."""

    cronologia.append({"role": "user", "content": messaggio})

    max_iterations = 30
    iteration = 0

    while iteration < max_iterations:
        iteration += 1

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
            cronologia.append({"role": "assistant", "content": response.content})

            # Esegui tool multipli IN PARALLELO
            if progress_callback and len(tool_uses) > 1:
                nomi = ", ".join(t.name for t in tool_uses)
                await progress_callback(f"Esecuzione parallela: {nomi}")

            async def run_tool(tool_use):
                if progress_callback:
                    await progress_callback(f"▶ {tool_use.name}...")
                result = await esegui_tool(tool_use.name, tool_use.input)
                if progress_callback:
                    stato = "✓" if not result.get("errore") else "✗"
                    await progress_callback(f"{stato} {tool_use.name} completato")
                return {
                    "type": "tool_result",
                    "tool_use_id": tool_use.id,
                    "content": json.dumps(result, ensure_ascii=False),
                }

            tool_results = await asyncio.gather(*[run_tool(t) for t in tool_uses])
            cronologia.append({"role": "user", "content": list(tool_results)})

        elif response.stop_reason == "max_tokens":
            cronologia.append({"role": "assistant", "content": response.content})
            if progress_callback:
                await progress_callback("Continuo l'elaborazione...")

        else:
            risposta_finale = f"Stop inatteso: {response.stop_reason}"
            cronologia.append({"role": "assistant", "content": risposta_finale})
            return risposta_finale, cronologia

    risposta_finale = "Limite iterazioni raggiunto (30). Task parzialmente completato."
    cronologia.append({"role": "assistant", "content": risposta_finale})
    return risposta_finale, cronologia
