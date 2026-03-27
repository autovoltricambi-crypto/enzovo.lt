import json
import asyncio
from typing import Optional
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
)
from tools.cataloghi import cerca_tutti_cataloghi, cerca_catalogo
from tools.prezzi import calcola_prezzo_vendita, scorporo_iva
from tools.csv_export import esporta_csv
from tools.memoria import salva_ricerca, cerca_in_memoria, salva_nota

Config.validate()

client = AsyncAnthropic(api_key=Config.ANTHROPIC_API_KEY)

# ==========================================
# DEFINIZIONE TOOL PER CLAUDE
# ==========================================

TOOLS = [
    {
        "name": "crea_prodotto",
        "description": "Crea un nuovo prodotto WooCommerce nel sito WordPress. Utile per aggiungere ricambi con titolo, prezzo, descrizione, stock, categoria.",
        "input_schema": {
            "type": "object",
            "properties": {
                "nome": {
                    "type": "string",
                    "description": "Nome del prodotto (es: 'Guarnizione Testata BMW N47')",
                },
                "prezzo": {
                    "type": "number",
                    "description": "Prezzo di listino (es: 45.50)",
                },
                "descrizione": {
                    "type": "string",
                    "description": "Descrizione dettagliata del prodotto",
                },
                "sku": {
                    "type": "string",
                    "description": "SKU/codice prodotto unico (es: 'GUAR-BMW-N47-001')",
                },
                "stock": {
                    "type": "integer",
                    "description": "Quantità in stock (default: 0)",
                },
                "categoria": {
                    "type": "string",
                    "description": "Nome categoria (es: 'Guarnizioni', 'Filtri', 'Oli')",
                },
            },
            "required": ["nome", "prezzo", "descrizione", "sku"],
        },
    },
    {
        "name": "modifica_prodotto",
        "description": "Modifica i dettagli di un prodotto esistente (titolo, prezzo, descrizione, stock, ecc.)",
        "input_schema": {
            "type": "object",
            "properties": {
                "product_id": {
                    "type": "integer",
                    "description": "ID del prodotto da modificare",
                },
                "nome": {
                    "type": "string",
                    "description": "Nuovo nome (opzionale)",
                },
                "prezzo": {
                    "type": "number",
                    "description": "Nuovo prezzo (opzionale)",
                },
                "descrizione": {
                    "type": "string",
                    "description": "Nuova descrizione (opzionale)",
                },
                "stock": {
                    "type": "integer",
                    "description": "Nuovo stock (opzionale)",
                },
            },
            "required": ["product_id"],
        },
    },
    {
        "name": "crea_pagina_html",
        "description": "Crea una nuova pagina HTML nel sito WordPress. Utile per creare landing page, pagine di prodotto personalizzate, guide.",
        "input_schema": {
            "type": "object",
            "properties": {
                "titolo": {
                    "type": "string",
                    "description": "Titolo della pagina (es: 'Catalogo BMW Ricambi')",
                },
                "contenuto_html": {
                    "type": "string",
                    "description": "Contenuto HTML completo della pagina (può includere CSS inline, div, tabelle, ecc.)",
                },
                "slug": {
                    "type": "string",
                    "description": "Slug URL (opzionale, es: 'catalogo-bmw')",
                },
                "stato": {
                    "type": "string",
                    "enum": ["draft", "publish"],
                    "description": "Stato pagina: 'draft' (bozza) o 'publish' (pubblica)",
                },
            },
            "required": ["titolo", "contenuto_html"],
        },
    },
    {
        "name": "scrivi_pagina_html",
        "description": "Modifica il contenuto HTML di una pagina WordPress esistente. Può anche modificare titolo e stato (bozza/pubblicata).",
        "input_schema": {
            "type": "object",
            "properties": {
                "page_id": {
                    "type": "integer",
                    "description": "ID della pagina da modificare",
                },
                "contenuto_html": {
                    "type": "string",
                    "description": "Nuovo contenuto HTML",
                },
                "titolo": {
                    "type": "string",
                    "description": "Nuovo titolo (opzionale)",
                },
                "stato": {
                    "type": "string",
                    "enum": ["draft", "publish"],
                    "description": "Stato pagina: 'draft' (bozza) o 'publish' (pubblica) — opzionale",
                },
            },
            "required": ["page_id", "contenuto_html"],
        },
    },
    {
        "name": "leggi_pagina_html",
        "description": "Legge il contenuto HTML di una pagina WordPress prima di modificarla.",
        "input_schema": {
            "type": "object",
            "properties": {
                "page_id": {
                    "type": "integer",
                    "description": "ID della pagina da leggere",
                },
            },
            "required": ["page_id"],
        },
    },
    {
        "name": "lista_prodotti",
        "description": "Elenca i prodotti nel sito con filtri opzionali per categoria o search.",
        "input_schema": {
            "type": "object",
            "properties": {
                "search": {
                    "type": "string",
                    "description": "Parola chiave per cercare (es: 'guarnizione')",
                },
                "categoria": {
                    "type": "string",
                    "description": "Filtra per categoria (opzionale)",
                },
                "limit": {
                    "type": "integer",
                    "description": "Max risultati (default 100)",
                },
            },
        },
    },
    {
        "name": "ispeziona_pagina_elementor",
        "description": "Legge i metadati Elementor di una pagina per ispezionarla. Utile prima di decidere se ricrearla in HTML.",
        "input_schema": {
            "type": "object",
            "properties": {
                "page_id": {
                    "type": "integer",
                    "description": "ID della pagina da ispezionare",
                },
            },
            "required": ["page_id"],
        },
    },
    {
        "name": "lista_pagine_elementor",
        "description": "Lista tutte le pagine del sito, distinguendo tra quelle create con Elementor e quelle in HTML puro.",
        "input_schema": {
            "type": "object",
            "properties": {},
        },
    },
    {
        "name": "cerca_tutti_cataloghi",
        "description": "Ricerca un prodotto su TUTTI i cataloghi B2B (Elring, Corteco, Valeo, AutoDoc). Restituisce prezzi comparati.",
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Nome prodotto, codice OE o descrizione (es: 'guarnizione testata BMW')",
                },
            },
            "required": ["query"],
        },
    },
    {
        "name": "cerca_catalogo",
        "description": "Ricerca un prodotto su un catalogo specifico (Elring, Corteco, Valeo, AutoDoc).",
        "input_schema": {
            "type": "object",
            "properties": {
                "catalogo": {
                    "type": "string",
                    "enum": ["Elring", "Corteco", "Valeo", "AutoDoc"],
                    "description": "Catalogo dove cercare",
                },
                "query": {
                    "type": "string",
                    "description": "Nome prodotto, codice OE o descrizione",
                },
            },
            "required": ["catalogo", "query"],
        },
    },
    {
        "name": "calcola_prezzo_vendita",
        "description": "Calcola prezzo di vendita da costo fornitore (applica margine + IVA automaticamente).",
        "input_schema": {
            "type": "object",
            "properties": {
                "costo": {
                    "type": "number",
                    "description": "Costo fornitore (es: 45.50)",
                },
                "margine": {
                    "type": "number",
                    "description": "Margine % (default 30%, opzionale)",
                },
                "iva": {
                    "type": "number",
                    "description": "IVA % (default 22%, opzionale)",
                },
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
                "prezzo_ivato": {
                    "type": "number",
                    "description": "Prezzo con IVA inclusa (es: 60.50)",
                },
                "iva": {
                    "type": "number",
                    "description": "IVA % (default 22%, opzionale)",
                },
            },
            "required": ["prezzo_ivato"],
        },
    },
    {
        "name": "esporta_csv",
        "description": "Esporta risultati di ricerca in formato CSV scaricabile.",
        "input_schema": {
            "type": "object",
            "properties": {
                "prodotti": {
                    "type": "array",
                    "description": "Lista di prodotti (dict con titolo, prezzo, fornitore, ecc.)",
                    "items": {"type": "object"},
                },
                "nome_file": {
                    "type": "string",
                    "description": "Nome file CSV (opzionale, senza .csv extension)",
                },
            },
            "required": ["prodotti"],
        },
    },
    {
        "name": "salva_ricerca",
        "description": "Salva una ricerca in memoria storica. Utile per ricordare cosa hai cercato.",
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Query di ricerca",
                },
                "catalogo": {
                    "type": "string",
                    "description": "Catalogo cercato",
                },
                "risultati_trovati": {
                    "type": "integer",
                    "description": "Numero risultati trovati",
                },
            },
            "required": ["query", "catalogo", "risultati_trovati"],
        },
    },
    {
        "name": "cerca_in_memoria",
        "description": "Cerca ricerche passate o note in memoria. Evita ricerche duplicate.",
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Cosa cercare in memoria",
                },
                "tipo": {
                    "type": "string",
                    "enum": ["ricerche", "prodotti", "note"],
                    "description": "Tipo di memoria da cercare",
                },
            },
            "required": ["query"],
        },
    },
    {
        "name": "salva_nota",
        "description": "Salva una nota personale per ricordarsi di qualcosa in futuro.",
        "input_schema": {
            "type": "object",
            "properties": {
                "titolo": {
                    "type": "string",
                    "description": "Titolo breve della nota",
                },
                "contenuto": {
                    "type": "string",
                    "description": "Contenuto/dettagli della nota",
                },
            },
            "required": ["titolo", "contenuto"],
        },
    },
]


# ==========================================
# ESECUZIONE TOOL
# ==========================================

async def esegui_tool(name: str, input_dict: dict) -> dict:
    """Esegue il tool e ritorna il risultato."""
    try:
        if name == "crea_prodotto":
            return await crea_prodotto(**input_dict)
        elif name == "modifica_prodotto":
            return await modifica_prodotto(**input_dict)
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
        elif name == "salva_ricerca":
            return salva_ricerca(**input_dict)
        elif name == "cerca_in_memoria":
            return cerca_in_memoria(**input_dict)
        elif name == "salva_nota":
            return salva_nota(**input_dict)
        else:
            return {"errore": f"Tool sconosciuto: {name}"}
    except Exception as e:
        return {"errore": f"Errore esecuzione {name}: {str(e)}"}


# ==========================================
# CICLO REACT PRINCIPALE
# ==========================================

async def chat(
    messaggio: str,
    cronologia: list = None,
    progress_callback=None,
) -> tuple[str, list]:
    """
    Loop ReAct semplice:
      1. Agente legge messaggio + cronologia
      2. Decide action (tool_use) o fine (text)
      3. Se tool_use: lo esegue e continua
      4. Se text: return risposta finale
    """
    if cronologia is None:
        cronologia = []

    # Aggiungi messaggio utente
    cronologia.append({"role": "user", "content": messaggio})

    system_prompt = """Sei un assistente intelligente per ricambi auto.
Puoi:
- Creare nuovi prodotti nel catalogo
- Modificare prodotti esistenti (prezzo, descrizione, stock)
- Creare pagine HTML personalizzate sul sito
- Cercare e leggere prodotti

Esegui le richieste dell'utente usando i tool disponibili.
Sii conciso e chiaro nelle risposte.
Sempre conferma le azioni completate."""

    max_iterations = 10
    iteration = 0

    while iteration < max_iterations:
        iteration += 1

        # Chiama Claude con i tool definiti
        response = await client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=4000,
            system=system_prompt,
            tools=TOOLS,
            messages=cronologia,
        )

        # Elabora risposta
        if response.stop_reason == "end_turn":
            # Claude ha finito: estrai testo e ritorna
            risposta_finale = ""
            for block in response.content:
                if hasattr(block, "text"):
                    risposta_finale = block.text
                    break

            cronologia.append({"role": "assistant", "content": risposta_finale})
            return risposta_finale, cronologia

        elif response.stop_reason == "tool_use":
            # Claude vuole usare un tool
            tool_uses = [b for b in response.content if b.type == "tool_use"]

            # Aggiungi assistant message con tutti i tool_use alla cronologia
            cronologia.append({"role": "assistant", "content": response.content})

            # Esegui tutti i tool_use e raccogli risultati
            tool_results = []
            for tool_use in tool_uses:
                if progress_callback:
                    await progress_callback(f"Esecuzione: {tool_use.name}({tool_use.input})")

                result = await esegui_tool(tool_use.name, tool_use.input)

                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": tool_use.id,
                    "content": json.dumps(result),
                })

                if progress_callback:
                    await progress_callback(f"{tool_use.name} completato")

            # Aggiungi tool_result alla cronologia
            cronologia.append({"role": "user", "content": tool_results})

        elif response.stop_reason == "max_tokens":
            # Claude ha raggiunto il limite di token — continua il ciclo
            cronologia.append({"role": "assistant", "content": response.content})
            if progress_callback:
                await progress_callback("Continuo l'elaborazione...")

        else:
            # Stop reason sconosciuto
            risposta_finale = f"Errore: stop_reason sconosciuto: {response.stop_reason}"
            cronologia.append({"role": "assistant", "content": risposta_finale})
            return risposta_finale, cronologia

    # Max iterazioni raggiunto
    risposta_finale = "Raggiunto limite iterazioni. Task non completato."
    cronologia.append({"role": "assistant", "content": risposta_finale})
    return risposta_finale, cronologia
