import json
import asyncio
import logging
from datetime import datetime
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
    cerca_prodotti_per_related_sku,
    aggiorna_descrizioni_bulk,
    aggiorna_prezzi_bulk,
    modifica_prodotto_completo,
    crea_post_blog,
    modifica_post_blog,
    lista_post_blog,
    crea_categoria_blog,
    lista_categorie_blog,
    leggi_impostazioni_wordpress,
    ispeziona_struttura_blog,
    crea_struttura_blog_completa,
    aggiungi_voce_menu,
    imposta_regola_categorie_blog,
)
from tools.cataloghi import cerca_tutti_cataloghi, cerca_catalogo, naviga_web, accedi_portale_b2b
from tools.design_components import (
    lista_componenti_premium,
    genera_blocchi_premium,
    genera_template_pagina_premium,
    revisiona_html_premium,
)
from tools.prezzi import calcola_prezzo_vendita, scorporo_iva
from tools.csv_export import esporta_csv, lista_csv_salvati, leggi_csv, modifica_csv, aggiungi_colonna_csv, modifica_csv_bulk
from tools.web_scraping import analizza_struttura_pagina, estrai_dati_con_playwright
from tools.memoria import (
    salva_ricerca,
    cerca_in_memoria,
    salva_nota,
    aggiorna_contesto_sito,
    leggi_contesto_sito,
    carica_contesto_agente,
    lista_knowledge,
    leggi_knowledge,
    aggiorna_knowledge,
    crea_knowledge,
    aggiorna_profilo,
    auto_aggiorna_profilo_da_testo,
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
        "description": (
            "Crea un nuovo prodotto WooCommerce nel sito. "
            "Quando prepari nome e descrizione, scrivi copy orientato alla conversione: "
            "hook iniziale, benefici chiari, compatibilita, rassicurazioni e CTA implicita. "
            "Evita muri di testo e frasi vaghe."
        ),
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
        "description": (
            "Crea una nuova pagina HTML premium nel sito WordPress. "
            "Il sistema applica automaticamente il design system AutoVolt (class=av). "
            "SCRIVI HTML RICCO e professionale, NON basico. Usa HTML semantico, mobile-first, DOM leggero, contrasto alto, copy chiaro e struttura pensata per conversione. Usa: "
            "<div class='av-hero'> per hero section con h1+p introduttivo, "
            "<div class='av-card'> per card, "
            "<div class='av-grid'> per layout a griglia di card, "
            "<a class='av-cta'> per pulsanti CTA rossi, "
            "<span class='av-badge'> per badge/etichette, "
            "<ul class='av-checklist'> per liste con check, "
            "<div class='av-info'> per box informativo blu, "
            "<div class='av-warn'> per box avviso giallo, "
            "<div class='av-stats'><div class='av-stat'><span class='av-stat-num'>42</span><span class='av-stat-label'>Prodotti</span></div></div> per statistiche, "
            "<hr class='av-sep'> per separatori eleganti, "
            "<blockquote> per callout evidenziati. "
            "Usa <table> con <th> per tabelle (stile zebra automatico). "
            "Usa <dl><dt><dd> per FAQ (stile card automatico). "
            "IMPORTANTE: scrivi almeno 3-4 sezioni con h2, contenuto ricco, "
            "almeno 1 CTA, almeno 1 card o grid. MAI pagine con solo testo piatto. La pagina deve essere comprensibile in pochi secondi e non dipendere da librerie JS pesanti."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "titolo": {"type": "string"},
                "contenuto_html": {"type": "string", "description": "HTML ricco e premium con classi av-*. Min 3 sezioni h2."},
                "slug": {"type": "string"},
                "stato": {"type": "string", "enum": ["draft", "publish"]},
            },
            "required": ["titolo", "contenuto_html"],
        },
    },
    {
        "name": "scrivi_pagina_html",
        "description": (
            "Modifica il contenuto HTML di una pagina WordPress esistente. "
            "Stesse regole di crea_pagina_html: scrivi HTML premium con classi av-* "
            "(av-hero, av-card, av-grid, av-cta, av-badge, av-checklist, av-info, av-stats, av-sep). "
            "Il design system viene applicato automaticamente. Mantieni la pagina semanticamente pulita, leggibile, veloce e orientata alla conversione."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "page_id": {"type": "integer"},
                "contenuto_html": {"type": "string", "description": "HTML ricco e premium con classi av-*."},
                "titolo": {"type": "string"},
                "stato": {"type": "string", "enum": ["draft", "publish"]},
            },
            "required": ["page_id", "contenuto_html"],
        },
    },
    {
        "name": "lista_componenti_premium",
        "description": (
            "Elenca la libreria di componenti premium disponibili e i template pagina supportati. "
            "Usalo prima di costruire home, landing, categoria o scheda prodotto importante."
        ),
        "input_schema": {"type": "object", "properties": {}},
    },
    {
        "name": "genera_blocchi_premium",
        "description": (
            "Assembla HTML premium da una lista di componenti riusabili. "
            "Supporta: hero, trust_strip, stats, feature_grid, split_section, price_box, testimonials, faq, cta_band, product_cards, checklist, logo_cloud. "
            "Usa questo tool quando vuoi comporre una pagina in modo strutturato invece di scrivere HTML libero da zero."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "titolo_pagina": {"type": "string", "description": "Titolo fallback se l'HTML risultante non contiene un H1."},
                "componenti": {
                    "type": "array",
                    "description": "Lista componenti. Ogni oggetto deve contenere almeno 'tipo' e i campi richiesti da quel componente.",
                    "items": {"type": "object"},
                },
            },
            "required": ["componenti"],
        },
    },
    {
        "name": "genera_template_pagina_premium",
        "description": (
            "Genera HTML premium da template predefiniti per pagine strategiche. "
            "Template supportati: home, landing, category, product. "
            "Questo deve essere il percorso preferito per pagine importanti: genera template, poi revisiona_html_premium, poi crea/scrivi la pagina."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "tipo_pagina": {"type": "string", "enum": ["home", "landing", "category", "product"]},
                "titolo": {"type": "string"},
                "sottotitolo": {"type": "string"},
                "badge": {"type": "string"},
                "cta_primaria_testo": {"type": "string"},
                "cta_primaria_url": {"type": "string"},
                "cta_secondaria_testo": {"type": "string"},
                "cta_secondaria_url": {"type": "string"},
                "trust_items": {"type": "array", "items": {"type": "string"}},
                "benefici": {"type": "array", "items": {"type": "string"}},
                "cards": {"type": "array", "items": {"type": "object"}},
                "stats": {"type": "array", "items": {"type": "object"}},
                "faq": {"type": "array", "items": {"type": "object"}},
                "testimonials": {"type": "array", "items": {"type": "object"}},
                "prezzo": {"type": "string"},
                "prezzo_note": {"type": "string"},
                "review_label": {"type": "string"},
                "image_url": {"type": "string"},
                "image_alt": {"type": "string"},
                "prodotti_correlati": {"type": "array", "items": {"type": "object"}},
                "intro_titolo": {"type": "string"},
                "intro_testo": {"type": "string"}
            },
            "required": ["tipo_pagina", "titolo"],
        },
    },
    {
        "name": "revisiona_html_premium",
        "description": (
            "Revisiona HTML di una pagina e assegna punteggi su chiarezza, design, conversione, performance e accessibilita. "
            "Usalo SEMPRE prima di pubblicare pagine strategiche. Se il punteggio totale e sotto 80, migliora l'HTML e rilancia la review."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "contenuto_html": {"type": "string", "description": "HTML da revisionare."},
                "tipo_pagina": {"type": "string", "enum": ["home", "landing", "category", "product"]},
            },
            "required": ["contenuto_html"],
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
    {
        "name": "analizza_struttura_pagina",
        "description": "Analizza l'HTML di una pagina per trovare selettori candidati e capire se conviene passare a Playwright dopo l'esplorazione con browser-use.",
        "input_schema": {
            "type": "object",
            "properties": {
                "url": {"type": "string"}
            },
            "required": ["url"],
        },
    },
    {
        "name": "estrai_dati_con_playwright",
        "description": "Estrae dati strutturati da una pagina renderizzata con Playwright. Usalo dopo aver capito la struttura della pagina.",
        "input_schema": {
            "type": "object",
            "properties": {
                "url": {"type": "string"},
                "selettori": {"type": "array", "items": {"type": "string"}},
                "limite": {"type": "integer"},
                "attesa_ms": {"type": "integer"}
            },
            "required": ["url"],
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
    {
        "name": "leggi_csv",
        "description": (
            "Legge un CSV dalla cartella exports/ e ritorna colonne e righe. "
            "Usalo per ispezionare il contenuto di un CSV prima di modificarlo. "
            "Ritorna max 50 righe (usa limite_righe=0 per tutte)."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "nome_file": {"type": "string", "description": "Nome del file CSV (es: 'prodotti_r304.csv')"},
                "limite_righe": {"type": "integer", "description": "Max righe da ritornare (default 50, 0=tutte)"},
            },
            "required": ["nome_file"],
        },
    },
    {
        "name": "modifica_csv",
        "description": (
            "Modifica celle specifiche di un CSV. "
            "Ogni modifica ha: riga (indice 0-based), colonna (nome), valore (nuovo valore). "
            "Crea nuove colonne automaticamente se non esistono."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "nome_file": {"type": "string"},
                "modifiche": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "riga": {"type": "integer", "description": "Indice riga (0-based, escluso header)"},
                            "colonna": {"type": "string", "description": "Nome colonna"},
                            "valore": {"type": "string", "description": "Nuovo valore"},
                        },
                        "required": ["riga", "colonna", "valore"],
                    },
                },
            },
            "required": ["nome_file", "modifiche"],
        },
    },
    {
        "name": "aggiungi_colonna_csv",
        "description": "Aggiunge una nuova colonna a un CSV esistente con un valore di default.",
        "input_schema": {
            "type": "object",
            "properties": {
                "nome_file": {"type": "string"},
                "nome_colonna": {"type": "string", "description": "Nome della nuova colonna"},
                "valore_default": {"type": "string", "description": "Valore di default per tutte le righe"},
            },
            "required": ["nome_file", "nome_colonna"],
        },
    },
    {
        "name": "modifica_csv_bulk",
        "description": (
            "Modifica una colonna su TUTTE le righe di un CSV (o solo quelle filtrate). "
            "Perfetto per aggiungere OEM o altri dati a tutte le righe. "
            "Es: modifica_csv_bulk('r304.csv', 'oem', '11427566327') setta OEM su tutte le righe. "
            "Con filtro: modifica_csv_bulk('r304.csv', 'oem', '123', 'marca', 'MANN') solo righe MANN."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "nome_file": {"type": "string"},
                "colonna": {"type": "string", "description": "Colonna da modificare o creare"},
                "valore": {"type": "string", "description": "Valore da assegnare"},
                "filtro_colonna": {"type": "string", "description": "Colonna per filtrare (opzionale)"},
                "filtro_valore": {"type": "string", "description": "Valore del filtro (opzionale)"},
            },
            "required": ["nome_file", "colonna", "valore"],
        },
    },
    # --- Ricerca e modifica prodotti avanzata ---
    {
        "name": "cerca_prodotti_per_related_sku",
        "description": (
            "Cerca tutti i prodotti WooCommerce con un dato related_sku_code. "
            "Es: cerca_prodotti_per_related_sku('R304') ritorna tutti i prodotti che vanno sugli stessi veicoli."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "related_sku_code": {"type": "string", "description": "Codice related_sku (es: 'R304')"},
            },
            "required": ["related_sku_code"],
        },
    },
    {
        "name": "aggiorna_descrizioni_bulk",
        "description": (
            "Aggiorna descrizione e/o nome di più prodotti WooCommerce in batch. "
            "Usa la batch API, molto più veloce di modificare uno alla volta."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "aggiornamenti": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "product_id": {"type": "integer"},
                            "descrizione": {"type": "string"},
                            "nome": {"type": "string"},
                        },
                        "required": ["product_id"],
                    },
                },
            },
            "required": ["aggiornamenti"],
        },
    },
    {
        "name": "aggiorna_prezzi_bulk",
        "description": (
            "Aggiorna prezzi di più prodotti WooCommerce in batch. "
            "Usalo dopo aver controllato i prezzi sul portale B2B del fornitore."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "aggiornamenti": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "product_id": {"type": "integer"},
                            "prezzo": {"type": "number", "description": "Nuovo prezzo (regular_price)"},
                            "prezzo_scontato": {"type": "number", "description": "Prezzo scontato (sale_price, opzionale)"},
                        },
                        "required": ["product_id", "prezzo"],
                    },
                },
            },
            "required": ["aggiornamenti"],
        },
    },
    {
        "name": "modifica_prodotto_completo",
        "description": (
            "Modifica completa di un prodotto WooCommerce: nome, prezzo, descrizione, "
            "descrizione_breve, stock, SKU, meta_data, immagini. "
            "Usa questo invece di modifica_prodotto quando devi toccare meta_data o immagini. "
            "Quando riscrivi descrizioni, usa copy persuasivo: problema, soluzione, benefici, compatibilita, fiducia e CTA."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "product_id": {"type": "integer"},
                "nome": {"type": "string"},
                "prezzo": {"type": "number"},
                "prezzo_scontato": {"type": "number"},
                "descrizione": {"type": "string"},
                "descrizione_breve": {"type": "string"},
                "stock": {"type": "integer"},
                "sku": {"type": "string"},
                "meta_data": {"type": "object", "description": "Chiave-valore da salvare come meta (es: {\"related_sku_code\": \"R304\"})"},
                "immagini": {"type": "array", "items": {"type": "string"}, "description": "Lista URL immagini prodotto"},
            },
            "required": ["product_id"],
        },
    },
    # --- Post Blog ---
    {
        "name": "crea_post_blog",
        "description": (
            "Crea un post blog WordPress (NON una pagina) per SEO. "
            "Usa per articoli su ricambi, guide, contenuti per posizionamento locale. "
            "Supporta categorie blog, tag, excerpt e immagine di copertina. "
            "SCRIVI HTML PREMIUM: usa h2 per sezioni, tabelle per confronti, "
            "dl/dt/dd per FAQ, blockquote per callout importanti, "
            "div.av-card per box informativi, ul.av-checklist per checklist, "
            "div.av-info per note, a.av-cta per CTA. "
            "Minimo 4 sezioni h2, contenuto ricco, almeno 1 tabella o card grid. Il testo deve essere scansionabile, chiaro, SEO-friendly ma anche persuasivo."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "titolo": {"type": "string"},
                "contenuto_html": {"type": "string", "description": "HTML premium con sezioni h2, tabelle, FAQ, card. Min 800 parole."},
                "slug": {"type": "string"},
                "stato": {"type": "string", "enum": ["draft", "publish"]},
                "categoria": {"type": "string", "description": "Nome categoria blog"},
                "tags": {"type": "array", "items": {"type": "string"}, "description": "Lista tag"},
                "excerpt": {"type": "string", "description": "Riassunto/descrizione breve per SEO"},
                "immagine_copertina": {"type": "string", "description": "URL immagine featured"},
            },
            "required": ["titolo", "contenuto_html"],
        },
    },
    {
        "name": "modifica_post_blog",
        "description": "Modifica un post blog WordPress esistente.",
        "input_schema": {
            "type": "object",
            "properties": {
                "post_id": {"type": "integer"},
                "titolo": {"type": "string"},
                "contenuto_html": {"type": "string"},
                "stato": {"type": "string", "enum": ["draft", "publish"]},
                "excerpt": {"type": "string"},
            },
            "required": ["post_id"],
        },
    },
    {
        "name": "lista_post_blog",
        "description": "Lista post blog del sito con filtri opzionali.",
        "input_schema": {
            "type": "object",
            "properties": {
                "search": {"type": "string"},
                "categoria": {"type": "string"},
                "limit": {"type": "integer"},
            },
        },
    },
    {
        "name": "crea_categoria_blog",
        "description": "Crea una categoria blog WordPress esplicita. Utile per strutturare il blog prima di creare gli articoli.",
        "input_schema": {
            "type": "object",
            "properties": {
                "nome": {"type": "string"},
                "slug": {"type": "string"},
                "descrizione": {"type": "string"},
                "parent_id": {"type": "integer", "description": "ID categoria padre opzionale"}
            },
            "required": ["nome"],
        },
    },
    {
        "name": "lista_categorie_blog",
        "description": "Lista le categorie blog WordPress disponibili.",
        "input_schema": {
            "type": "object",
            "properties": {
                "search": {"type": "string"},
                "limit": {"type": "integer"}
            },
        },
    },
    {
        "name": "leggi_impostazioni_wordpress",
        "description": "Legge le impostazioni principali di WordPress: home, pagina blog, posts per page e categoria di default.",
        "input_schema": {"type": "object", "properties": {}},
    },
    {
        "name": "ispeziona_struttura_blog",
        "description": "Analizza la struttura reale del blog: pagina articoli, categorie esistenti, post senza categoria utile e categorie mancanti.",
        "input_schema": {"type": "object", "properties": {}},
    },
    {
        "name": "crea_struttura_blog_completa",
        "description": "Crea la struttura base del blog per Auto-Volt con categorie principali e salva la decisione in memoria.",
        "input_schema": {
            "type": "object",
            "properties": {
                "categorie": {"type": "array", "items": {"type": "string"}, "description": "Lista opzionale di categorie blog da creare"}
            },
        },
    },
    {
        "name": "aggiungi_voce_menu",
        "description": (
            "Aggiunge una voce a un menu WordPress (location: primary, secondary_menu, footer_menu, mobile_menu). "
            "Evita duplicati. Usalo per collegare pagine, categorie, link custom al menu del sito. "
            "Esempio: collegare /magazine-auto/ al menu principale del sito."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "titolo": {"type": "string", "description": "Testo visibile nel menu (es: 'Magazine AutoVolt')"},
                "url": {"type": "string", "description": "URL della voce menu (es: 'https://auto-volt.it/magazine-auto/')"},
                "menu_location": {"type": "string", "description": "Posizione menu: primary (default), secondary_menu, footer_menu, mobile_menu"},
                "menu_id": {"type": "integer", "description": "ID del menu specifico se noto (opzionale)"},
                "menu_slug": {"type": "string", "description": "Slug del menu (es: 'primary') se non usi menu_location"},
                "parent_id": {"type": "integer", "description": "ID voce padre per sottovoci (default 0)"},
                "menu_order": {"type": "integer", "description": "Posizione nell'ordine (calcolata automaticamente se omessa)"},
                "object_id": {"type": "integer", "description": "ID WP della pagina/post/categoria se tipo='post_type'"},
                "object_type": {"type": "string", "description": "Tipo oggetto: 'page', 'post', 'category'. Default 'page'"},
                "item_type": {"type": "string", "description": "Tipo voce: 'post_type', 'taxonomy', 'custom'. Default 'custom' (link libero)"},
            },
            "required": ["titolo", "url"],
        },
    },
    {
        "name": "imposta_regola_categorie_blog",
        "description": (
            "Configura le regole di auto-assegnazione delle categorie blog. "
            "Da questo momento, ogni articolo creato senza categoria esplicita viene assegnato automaticamente "
            "alla categoria giusta in base alle parole chiave nel titolo e nel testo. "
            "Usalo anche solo con attiva=true per attivare le regole predefinite."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "regole": {
                    "type": "object",
                    "description": "Dict opzionale: {nome_categoria: [lista keyword]}. Se omesso usa le regole predefinite del sistema.",
                    "additionalProperties": {"type": "array", "items": {"type": "string"}}
                },
                "attiva": {"type": "boolean", "description": "Attiva o disattiva la classificazione automatica (default true)"}
            },
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
    # --- Profilo Utente ---
    {
        "name": "aggiorna_profilo",
        "description": (
            "Aggiorna il profilo dell'utente con informazioni personali e preferenze. "
            "Usalo quando l'utente si presenta, dice il suo nome, descrive la sua attività, "
            "o comunica preferenze. Salva SUBITO senza chiedere conferma. "
            "Campi standard: nome, attivita, settore, budget_mensile, obiettivo_principale, preferenze, note_personali. "
            "Puoi aggiungere campi custom."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "nome": {"type": "string", "description": "Nome dell'utente"},
                "attivita": {"type": "string", "description": "Tipo di attività (es: negozio ricambi auto)"},
                "settore": {"type": "string", "description": "Settore di riferimento"},
                "budget_mensile": {"type": "string", "description": "Budget mensile disponibile"},
                "obiettivo_principale": {"type": "string", "description": "Obiettivo principale attuale"},
                "preferenze": {"type": "string", "description": "Preferenze varie (margine, stile comunicazione, ecc.)"},
                "note_personali": {"type": "string", "description": "Note libere sull'utente"},
            },
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
    """Esegue un tool con timeout più lungo per browser e Playwright."""
    try:
        coro = _dispatch_tool(name, input_dict)
        timeout = 180 if name in {"naviga_web", "accedi_portale_b2b", "cerca_catalogo", "cerca_tutti_cataloghi", "estrai_dati_con_playwright"} else 60
        return await asyncio.wait_for(coro, timeout=timeout)
    except asyncio.TimeoutError:
        return {"errore": f"Tool '{name}' ha superato il timeout di {timeout} secondi"}
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
    elif name == "lista_componenti_premium":
        return lista_componenti_premium()
    elif name == "genera_blocchi_premium":
        return genera_blocchi_premium(**input_dict)
    elif name == "genera_template_pagina_premium":
        return genera_template_pagina_premium(**input_dict)
    elif name == "revisiona_html_premium":
        return revisiona_html_premium(**input_dict)
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
    elif name == "analizza_struttura_pagina":
        return await analizza_struttura_pagina(**input_dict)
    elif name == "estrai_dati_con_playwright":
        return await estrai_dati_con_playwright(**input_dict)
    elif name == "calcola_prezzo_vendita":
        return calcola_prezzo_vendita(**input_dict)
    elif name == "scorporo_iva":
        return scorporo_iva(**input_dict)
    elif name == "esporta_csv":
        return esporta_csv(**input_dict)
    elif name == "lista_csv_salvati":
        return lista_csv_salvati()
    elif name == "leggi_csv":
        return leggi_csv(**input_dict)
    elif name == "modifica_csv":
        return modifica_csv(**input_dict)
    elif name == "aggiungi_colonna_csv":
        return aggiungi_colonna_csv(**input_dict)
    elif name == "modifica_csv_bulk":
        return modifica_csv_bulk(**input_dict)
    elif name == "cerca_prodotti_per_related_sku":
        return await cerca_prodotti_per_related_sku(**input_dict)
    elif name == "aggiorna_descrizioni_bulk":
        return await aggiorna_descrizioni_bulk(**input_dict)
    elif name == "aggiorna_prezzi_bulk":
        return await aggiorna_prezzi_bulk(**input_dict)
    elif name == "modifica_prodotto_completo":
        return await modifica_prodotto_completo(**input_dict)
    elif name == "crea_post_blog":
        return await crea_post_blog(**input_dict)
    elif name == "modifica_post_blog":
        return await modifica_post_blog(**input_dict)
    elif name == "lista_post_blog":
        return await lista_post_blog(**input_dict)
    elif name == "crea_categoria_blog":
        return await crea_categoria_blog(**input_dict)
    elif name == "lista_categorie_blog":
        return await lista_categorie_blog(**input_dict)
    elif name == "leggi_impostazioni_wordpress":
        return await leggi_impostazioni_wordpress()
    elif name == "ispeziona_struttura_blog":
        return await ispeziona_struttura_blog()
    elif name == "crea_struttura_blog_completa":
        return await crea_struttura_blog_completa(**input_dict)
    elif name == "aggiungi_voce_menu":
        return await aggiungi_voce_menu(**input_dict)
    elif name == "imposta_regola_categorie_blog":
        return await imposta_regola_categorie_blog(**input_dict)
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
    elif name == "aggiorna_profilo":
        return aggiorna_profilo(**input_dict)
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

    # Estrae già dal messaggio corrente sito, stack tecnico e preferenze operative.
    auto_aggiorna_profilo_da_testo(messaggio)

    # Data e ora corrente
    _now = datetime.now()
    _data_ora = _now.strftime("%A %d %B %Y, ore %H:%M")
    _giorno_settimana = _now.strftime("%A")

    # Carica contesto persistente dalla memoria
    contesto = carica_contesto_agente()

    # Carica profilo utente
    from tools.memoria import carica_profilo
    _profilo = carica_profilo()
    _profilo_str = ""
    if _profilo:
        righe_p = []
        for k, v in _profilo.items():
            if v:  # skip campi vuoti
                righe_p.append(f"- {k}: {v}")
        _profilo_str = "\n".join(righe_p) if righe_p else "Profilo vuoto — chiedi all'utente di presentarsi."
    else:
        _profilo_str = "Profilo vuoto — chiedi all'utente di presentarsi."

    # Carica indice CSV disponibili
    from tools.csv_export import lista_csv_salvati
    _csv_index = lista_csv_salvati()
    _csv_list = _csv_index.get("csv", [])
    if _csv_list:
        _csv_str = "\n".join(f"- {c['file']}: {c.get('descrizione', '')} ({c.get('righe', '?')} righe, {c.get('data', '')[:10]})" for c in _csv_list[-10:])
    else:
        _csv_str = "Nessun CSV esportato ancora."

    # Carica riepiloghi sessioni precedenti
    from tools.memoria import carica_ultimi_riepiloghi
    _riepiloghi = carica_ultimi_riepiloghi(3)
    if _riepiloghi:
        _riep_str = "\n".join(
            f"- {r.get('data', '')[:16]}: {r.get('riepilogo', '')[:200]}"
            for r in _riepiloghi
        )
    else:
        _riep_str = "Nessuna sessione precedente registrata."

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
    for fname in ("azcar-import.md", "plugin-compatibilita.md", "adhd-guida.md", "agente-motivazione.md", "workflow-agente-completo.md", "ricambi.md", "prompt-engineering-basi.md"):
        r = leggi_knowledge(fname)
        if "contenuto" in r:
            _know_critico += f"\n\n--- {fname} ---\n{r['contenuto']}"

    # Lista di tutti i knowledge file disponibili CON INDICE CATEGORIZZATO
    _know_lista = lista_knowledge()
    _know_files = ", ".join(_know_lista.get("files", [])) or "nessuno"

    # Mappa argomento → file knowledge per guidare l'agente
    _know_indice = """
INDICE KNOWLEDGE PER ARGOMENTO (usa leggi_knowledge per leggere):

SEO:
  - seo.md, seo-fondamenti.md, seo-keyword-research.md, seo-on-page.md, seo-tecnico.md
  - seo-ecommerce.md, seo-ricambi-auto.md, local-seo.md, link-building.md

GOOGLE ADS:
  - google-ads-search.md, google-ads-shopping.md, google-ads-display.md
  - google-ads-youtube.md, google-ads-remarketing.md, google-ads-performance-max.md
  - google-ads-bid-strategy.md, google-ads-quality-score.md

META ADS (Facebook/Instagram):
  - meta-ads-fondamenti.md, meta-ads-targeting.md, meta-ads-creativita.md
  - meta-ads-budget.md, meta-ads-retargeting.md

EMAIL MARKETING:
  - email-marketing-fondamenti.md, email-marketing-copywriting.md
  - email-marketing-automation.md, email-marketing-segmentazione.md

ECOMMERCE:
  - ecommerce-strategia.md, ecommerce-funnel.md, ecommerce-pricing.md
  - ecommerce-retention.md, marketplace-amazon.md

CRO (Conversioni):
  - cro-fondamenti.md, cro-ab-testing.md, cro-ecommerce.md

COPYWRITING:
  - copywriting-fondamenti.md, copywriting-ads.md, descrizioni-prodotto.md

CONTENT MARKETING:
  - content-marketing-strategia.md, content-marketing-blog.md

SOCIAL MEDIA:
  - social-media-strategia.md, social-media-instagram.md
  - social-media-tiktok.md, social-media-youtube.md

ANALYTICS:
  - analytics-ga4.md, analytics-kpi.md, analytics-attribuzione.md

MARKETING AUTOMATION:
  - marketing-automation-fondamenti.md, marketing-automation-crm.md

RICAMBI AUTO & OPERATIVO AGENTE:
  - ricambi.md (info settore ricambi auto)
  - plugin-compatibilita.md (plugin compatibilità veicoli WooCommerce)
  - oem-cross-reference.md (codici OEM, cross-reference, come trovarli e usarli)
  - csv-workflow.md (lavorare con CSV: struttura, import/export, modifiche)
  - aggiornamento-prezzi-b2b.md (workflow prezzi da portali B2B, ricarichi, margini)
  - woocommerce-api-tips.md (tips WooCommerce REST API, meta_data, batch, errori)
  - blog-seo-ricambi.md (scrivere articoli blog SEO per ricambi auto)
  - workflow-agente-completo.md (guida operativa completa: tutti i workflow step-by-step)
  - azcar-import.md (navigazione portale AZ Car)

SVILUPPO WEB & DEBUG:
    - html-css-basi.md (HTML e CSS base)
    - javascript-basi.md (DOM, eventi, fetch, render UI)
    - responsive-mobile.md (responsive mobile-first per smartphone)
    - debug-frontend-wordpress.md (debug frontend, fetch, DOM, WordPress, blog archive)
    - scraping-web-strategie.md (quando usare browser-use e quando passare a Playwright)
    - prompt-engineering-basi.md (interpretazione richieste, contesto, assunzioni, azione)

ALTRO:
  - influencer-marketing.md, affiliate-marketing.md
  - economia-macro-micro.md, economia-imprese.md, gestione-impresa.md
  - legge-dipendenti-italia.md
  - ads.md (advertising generale)
"""

    system_prompt = f"""Sei un agente AI autonomo, esperto e motivato. Puoi fare qualsiasi \
cosa: navigare il web, gestire sistemi, scrivere codice, analizzare dati, risolvere problemi \
tecnici, creare contenuti, fare ricerche approfondite, automatizzare processi e molto altro.

## Identità e modo di operare

Sei un esperto informatico full-stack con competenze avanzate di HTML, CSS, JavaScript, \
web performance, Core Web Vitals, UX persuasiva, CRO, copywriting web e teoria dei colori. \
Quando crei pagine o articoli HTML per WordPress, scrivi SEMPRE codice premium: \
layout moderni con hero section, card grid, CTA, tabelle stilizzate, FAQ eleganti. \
MAI HTML basico con solo h1+p. Usa le classi del design system (av-hero, av-card, av-grid, \
av-cta, av-badge, av-checklist, av-info, av-warn, av-stats, av-sep, blockquote per callout). \
Ogni pagina deve essere comprensibile in 3-5 secondi, semanticamente pulita, mobile-first, \
ad alto contrasto, con palette coerente, CTA specifiche, gerarchia visiva chiara e attenzione a LCP, INP e CLS. \
Per pagine strategiche NON improvvisare HTML libero come prima scelta: \
1) usa lista_componenti_premium se ti serve la libreria disponibile, \
2) usa genera_template_pagina_premium o genera_blocchi_premium per costruire la struttura, \
3) usa revisiona_html_premium, \
4) se il punteggio totale e sotto 80 migliora il markup e ripeti la review, \
5) solo dopo usa crea_pagina_html o scrivi_pagina_html. \
Il tuo approccio:

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

=== REGOLA CRITICA: CONSULTA SEMPRE I KNOWLEDGE ===
PRIMA di rispondere su qualsiasi argomento per cui esiste un file knowledge, DEVI:
1. Guardare l'indice sotto per trovare i file rilevanti
2. Chiamare leggi_knowledge(nome_file) per ognuno
3. Solo DOPO aver letto i file, formulare la risposta

NON rispondere MAI basandoti solo sulle tue conoscenze generali quando hai un file specifico.
Se l'utente chiede di SEO → leggi i file SEO. Se chiede di Google Ads → leggi i file Google Ads.
Se chiede di ricambi → leggi ricambi.md. E così via.

{_know_indice}

File disponibili: {_know_files}
====================================================

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

=== DATA E ORA CORRENTE ===
{_data_ora} ({_giorno_settimana})
===========================

=== PROFILO UTENTE ===
{_profilo_str}
Se il profilo è vuoto o incompleto, chiedi all'utente le info base (nome, attività, budget)
e salvale con aggiorna_profilo.
======================

=== CSV ESPORTATI (ultimi 10) ===
{_csv_str}
Usa lista_csv_salvati() per la lista completa.
=================================

=== CONTESTO (memoria sessioni precedenti) ===
{contesto}
==============================================

=== SESSIONI PRECEDENTI (riepiloghi) ===
{_riep_str}
=========================================

Hai accesso a tool per:
- Navigare e interagire con qualsiasi sito web (naviga_web, accedi_portale_b2b)
- Analizzare struttura HTML e fare scraping strutturato con Playwright
- Gestire un sito WordPress/WooCommerce (prodotti, categorie, pagine)
- Cercare su cataloghi B2B e portali fornitore
- Calcolare prezzi, esportare CSV
- Leggere knowledge base di riferimento (leggi_knowledge)
- Salvare memoria, contesto e profilo utente tra sessioni

Quando ricevi un task complesso:
1. ANALIZZA: capisci il problema a fondo — cosa serve esattamente? Cosa potrebbe andare storto?
2. PIANIFICA: descrivi i passi che farai (numerati)
3. ESEGUI: usa i tool, in parallelo dove possibile, senza aspettare conferme per ogni step
4. VERIFICA: controlla il risultato — è quello che ci si aspettava? C'è qualcosa che non torna?
5. MEMORIZZA: salva decisioni importanti con aggiorna_contesto_sito

Per task semplici rispondi direttamente senza pianificazione.
Se qualcosa non funziona, diagnostica prima di cambiare approccio.

=== PROTOCOLLO DI INTERPRETAZIONE UTENTE ===

Ogni messaggio dell'utente va interpretato prima di essere eseguito.
Non limitarti alla frase letterale: usa il contesto della sessione, la memoria,
il profilo utente, i task attivi e i knowledge file per capire il significato reale.

Prima di agire, ricava mentalmente:
1. Obiettivo reale dell'utente
2. Contesto già disponibile
3. Vincoli e preferenze implicite o esplicite
4. Dati davvero mancanti
5. Miglior azione possibile adesso

REGOLE:
- Se la richiesta è breve ma il contesto è sufficiente, interpreta e procedi.
- Se manca solo un dettaglio secondario, fai un'assunzione ragionevole e dichiarala brevemente.
- Se l'ambiguità rischia di produrre lavoro sbagliato, fai una sola domanda mirata.
- Evita di chiedere cose già presenti in memoria o nel contesto.
- Quando l'utente scrive in modo informale o ellittico, collegati sempre agli ultimi task attivi.

Quando utile, esplicita in una frase l'interpretazione che stai usando, poi esegui.
Esempio: "Interpreto questa richiesta come un miglioramento frontend mobile-first, quindi procedo su layout e responsive."

Per richieste su frontend, interfacce o modifiche UI, leggi sempre:
- html-css-basi.md
- javascript-basi.md
- responsive-mobile.md
- debug-frontend-wordpress.md

Per scraping web e raccolta dati da pagine:
- se il sito è sconosciuto o interattivo, esplora prima con naviga_web
- poi usa analizza_struttura_pagina per trovare selettori candidati
- se serve estrazione precisa o ripetibile, passa a estrai_dati_con_playwright
- consulta scraping-web-strategie.md

Per richieste ambigue o implicite, consulta anche:
- prompt-engineering-basi.md
================================================

=== AUTO-MEMORIA (salva fatti importanti automaticamente) ===

Quando durante la conversazione l'utente rivela informazioni importanti, SALVALE SUBITO
senza chiedere conferma. Non aspettare che te lo chieda. Esempi:

- L'utente dice il suo nome o parla della sua attività → aggiorna_profilo(nome=..., attivita=...)
- L'utente comunica un budget o una preferenza → aggiorna_profilo(budget_mensile=..., preferenze=...)
- Se dal messaggio emergono stack tecnico, sito, CMS, WooCommerce, HTML/CSS/JS, esigenze mobile o preferenze operative → aggiorna_profilo(stack_tecnico=..., preferenze_tecniche=..., sito_web=...)
- Viene presa una decisione sul sito (margine, struttura, ecc.) → aggiorna_contesto_sito(chiave, valore)
- Trovi un'informazione utile durante una ricerca → salva_nota(titolo, contenuto)
- Crei un prodotto su WooCommerce → il tracciamento è automatico, non devi fare nulla

Regola d'oro: se un'informazione potrebbe servire nella prossima sessione, salvala ORA.
=============================================================

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
                        if result.get("modello_usato"):
                            await progress_callback(f"ℹ {tool_use.name}: modello {result['modello_usato']}")
                        tentativi = result.get("tentativi") or []
                        if tentativi:
                            dettagli = "; ".join(
                                f"{t.get('modello', '?')} ({t.get('max_steps', '?')} step)" if t.get('max_steps') else t.get('modello', '?')
                                for t in tentativi
                            )
                            await progress_callback(f"ℹ {tool_use.name}: fallback provati -> {dettagli}")
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
