"""Operazioni WordPress/WooCommerce via REST API."""
import asyncio
import json
import re
import unicodedata
import httpx
from tools.cataloghi import get_wp_client
from tools.memoria import salva_prodotto_in_memoria, aggiorna_contesto_sito, leggi_contesto_sito


DEFAULT_BLOG_CATEGORY_RULES = {
    "Guide Ricambi": [
        "quale",
        "guida",
        "compatibile",
        "compatibil",
        "codice oe",
        "codice oem",
        "ricambio",
        "filtro",
        "pastiglie",
        "batteria",
        "panda",
        "500",
        "clio",
        "golf",
    ],
    "Manutenzione Auto": [
        "manutenzione",
        "tagliando",
        "cambiare",
        "sostituire",
        "ogni quanto",
        "quando cambiare",
        "olio motore",
        "filtro aria",
        "filtro abitacolo",
        "revisione",
        "controllare",
    ],
    "Problemi e Diagnosi": [
        "spia",
        "problema",
        "diagnosi",
        "errore",
        "sintomo",
        "non parte",
        "rumore",
        "vibra",
        "perde potenza",
        "fumosita",
        "accesa",
        "guasto",
    ],
    "Confronti e Recensioni": [
        "vs",
        "confronto",
        "recensione",
        "migliore",
        "meglio",
        "differenza",
        "mann",
        "mahle",
        "ufi",
        "bosch",
    ],
    "News Auto Elettriche": [
        "elettrica",
        "elettriche",
        "bev",
        "batterie",
        "ricarica",
        "colonnina",
        "plug-in",
        "plug in",
        "ibrida",
        "ev",
        "mobilita elettrica",
    ],
}


_AV_DESIGN_CSS = """<style>
/* === AutoVolt Premium Design System v2 === */
.av{font-family:'Inter',-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;color:#1f2937;background:#fff;line-height:1.75;font-size:1.05rem;max-width:820px;margin:0 auto;padding:2.5rem 2rem}
/* Typography */
.av h1{font-size:2.25rem;font-weight:800;color:#0f172a;line-height:1.2;margin:0 0 1.25rem;letter-spacing:-.02em}
.av h2{font-size:1.5rem;font-weight:700;color:#1e293b;margin:2.5rem 0 1rem;padding-bottom:.5rem;border-bottom:3px solid #dc2626}
.av h3{font-size:1.2rem;font-weight:600;color:#334155;margin:2rem 0 .75rem}
.av h4{font-size:1.05rem;font-weight:600;color:#475569;margin:1.5rem 0 .5rem}
.av p{margin:0 0 1.25rem}
.av strong{color:#0f172a}
.av em{color:#64748b}
/* Links */
.av a{color:#dc2626;text-decoration:none;border-bottom:1px solid transparent;transition:border-color .2s,color .2s}
.av a:hover{border-bottom-color:#dc2626;color:#991b1b}
/* Lists */
.av ul,.av ol{margin:0 0 1.5rem 1.25rem}
.av li{margin-bottom:.5rem}
.av ul li::marker{color:#dc2626;font-weight:700}
/* Tables — zebra + hover */
.av table{width:100%;border-collapse:separate;border-spacing:0;margin:1.5rem 0;border-radius:10px;overflow:hidden;box-shadow:0 1px 4px rgba(0,0,0,.08)}
.av th{background:#1e293b;color:#fff;font-weight:600;text-align:left;padding:12px 16px;font-size:.92rem;text-transform:uppercase;letter-spacing:.04em}
.av td{padding:11px 16px;border-bottom:1px solid #e2e8f0}
.av tr:nth-child(even) td{background:#f8fafc}
.av tr:last-child td{border-bottom:none}
.av tr:hover td{background:#f1f5f9}
/* FAQ (dl/dt/dd) — card-style */
.av dl{margin:1.5rem 0}
.av dt{font-weight:700;color:#1e293b;margin-top:1rem;padding:1rem 1.25rem .5rem;background:#f8fafc;border-left:4px solid #dc2626;border-radius:0 8px 0 0}
.av dd{margin:0 0 .75rem;padding:.5rem 1.25rem 1rem;background:#f8fafc;border-left:4px solid #dc2626;border-radius:0 0 8px 0}
/* Blockquote — callout */
.av blockquote{background:linear-gradient(135deg,#fef2f2,#fff1f2);border-left:4px solid #dc2626;padding:1.25rem 1.5rem;margin:1.5rem 0;border-radius:0 10px 10px 0;font-style:normal}
.av blockquote p:last-child{margin-bottom:0}
/* Images */
.av img{max-width:100%;height:auto;border-radius:12px;margin:1.5rem 0;box-shadow:0 4px 15px rgba(0,0,0,.08)}
/* === Utility classes (opzionali, l'agente puo usarli) === */
/* Hero */
.av .av-hero{text-align:center;padding:2.5rem 0 2rem;margin-bottom:2rem;border-bottom:1px solid #e2e8f0}
.av .av-hero h1{font-size:2.6rem;margin-bottom:.75rem}
.av .av-hero p{font-size:1.15rem;color:#64748b;max-width:600px;margin:0 auto}
/* Card */
.av .av-card{background:#f8fafc;border:1px solid #e2e8f0;border-radius:12px;padding:1.5rem;margin:1rem 0;transition:box-shadow .2s}
.av .av-card:hover{box-shadow:0 4px 12px rgba(0,0,0,.06)}
.av .av-card h3{margin-top:0;color:#1e293b}
/* Grid */
.av .av-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:1.25rem;margin:1.5rem 0}
/* CTA Button */
.av .av-cta{display:inline-block;background:#dc2626;color:#fff!important;padding:14px 32px;border-radius:8px;font-weight:700;text-decoration:none!important;border:none;border-bottom:none!important;font-size:1rem;transition:background .2s,transform .1s;cursor:pointer}
.av .av-cta:hover{background:#b91c1c;transform:translateY(-1px);color:#fff!important}
/* Badge */
.av .av-badge{display:inline-block;background:#fef2f2;color:#dc2626;padding:4px 12px;border-radius:20px;font-size:.8rem;font-weight:600}
/* Checklist */
.av .av-checklist{list-style:none;margin-left:0;padding-left:0}
.av .av-checklist li{padding:.5rem 0 .5rem 2rem;position:relative}
.av .av-checklist li::before{content:'✓';position:absolute;left:0;color:#dc2626;font-weight:700;font-size:1.1rem}
/* Separator */
.av .av-sep{border:none;height:2px;background:linear-gradient(90deg,transparent,#e2e8f0,transparent);margin:2.5rem 0}
/* Info box */
.av .av-info{background:#eff6ff;border:1px solid #bfdbfe;border-radius:10px;padding:1rem 1.25rem;margin:1.5rem 0;color:#1e40af}
.av .av-info strong{color:#1e3a8a}
/* Warning box */
.av .av-warn{background:#fefce8;border:1px solid #fde68a;border-radius:10px;padding:1rem 1.25rem;margin:1.5rem 0;color:#92400e}
/* Stats row */
.av .av-stats{display:flex;gap:1rem;flex-wrap:wrap;margin:1.5rem 0}
.av .av-stat{flex:1;min-width:120px;text-align:center;background:#f8fafc;border:1px solid #e2e8f0;border-radius:10px;padding:1.25rem .75rem}
.av .av-stat .av-stat-num{display:block;font-size:1.75rem;font-weight:800;color:#dc2626}
.av .av-stat .av-stat-label{font-size:.8rem;color:#64748b;text-transform:uppercase;letter-spacing:.05em}
/* Responsive */
@media(max-width:640px){
.av{padding:1.25rem 1rem;font-size:1rem}
.av h1{font-size:1.75rem}
.av h2{font-size:1.3rem}
.av .av-hero h1{font-size:2rem}
.av table{font-size:.9rem}
.av th,.av td{padding:8px 10px}
.av .av-grid{grid-template-columns:1fr}
.av .av-stats{flex-direction:column}
}
</style>"""


def _ensure_accessible_html_contrast(contenuto_html: str) -> str:
    """Wrappa il contenuto HTML nel design system premium AutoVolt."""
    if not contenuto_html or not contenuto_html.strip():
        return contenuto_html

    # Evita doppio wrapping
    if 'class="av"' in contenuto_html or "class='av'" in contenuto_html:
        return contenuto_html

    # Compatibilità: rimuovi vecchio wrapper se presente
    contenuto_html = contenuto_html.replace(
        '<div class="autovolt-readable-content">', ""
    ).replace("</div><!-- /autovolt-readable-content -->", "")
    if "autovolt-readable-content" in contenuto_html:
        contenuto_html = re.sub(
            r'<div class="autovolt-readable-content">(.*?)</div>\s*$',
            r"\1",
            contenuto_html,
            flags=re.DOTALL,
        )

    return f'{_AV_DESIGN_CSS}\n<div class="av">\n{contenuto_html}\n</div>'


# ==========================================
# PRODOTTI WOOCOMMERCE
# ==========================================

async def crea_prodotto(
    nome: str,
    prezzo: float,
    descrizione: str,
    sku: str,
    stock: int = 0,
    categoria: str | None = None,
    related_sku_code: str | None = None,
) -> dict:
    """Crea un nuovo prodotto WooCommerce."""
    client = get_wp_client()

    payload = {
        "name": nome,
        "regular_price": str(prezzo),
        "description": descrizione,
        "sku": sku,
        "manage_stock": True,
        "stock_quantity": stock,
        "status": "publish",
    }

    if related_sku_code:
        payload["meta_data"] = [{"key": "related_sku_code", "value": related_sku_code}]

    if categoria:
        # Cerca o crea la categoria
        cat_id = await _get_or_create_categoria(client, categoria)
        if cat_id:
            payload["categories"] = [{"id": cat_id}]

    r = await client.post("/wp-json/wc/v3/products", json=payload)
    if r.status_code in (200, 201):
        data = r.json()
        risultato = {
            "successo": True,
            "id": data["id"],
            "nome": data["name"],
            "prezzo": data["regular_price"],
            "sku": data["sku"],
        }
        # Traccia in memoria locale
        salva_prodotto_in_memoria(risultato)
        return risultato
    return {"errore": f"HTTP {r.status_code}: {r.text[:200]}"}


async def modifica_prodotto(
    product_id: int,
    nome: str | None = None,
    prezzo: float | None = None,
    descrizione: str | None = None,
    stock: int | None = None,
) -> dict:
    """Modifica un prodotto WooCommerce esistente."""
    client = get_wp_client()

    payload = {}
    if nome is not None:
        payload["name"] = nome
    if prezzo is not None:
        payload["regular_price"] = str(prezzo)
    if descrizione is not None:
        payload["description"] = descrizione
    if stock is not None:
        payload["stock_quantity"] = stock
        payload["manage_stock"] = True

    r = await client.put(f"/wp-json/wc/v3/products/{product_id}", json=payload)
    if r.status_code == 200:
        data = r.json()
        return {
            "successo": True,
            "id": data["id"],
            "nome": data["name"],
            "prezzo": data["regular_price"],
        }
    return {"errore": f"HTTP {r.status_code}: {r.text[:200]}"}


async def lista_prodotti(
    search: str | None = None,
    categoria: str | None = None,
    limit: int = 100,
) -> dict:
    """Elenca prodotti WooCommerce con filtri opzionali."""
    client = get_wp_client()

    params: dict = {"per_page": min(limit, 100)}
    if search:
        params["search"] = search
    if categoria:
        # Trova ID categoria
        r_cat = await client.get("/wp-json/wc/v3/products/categories", params={"search": categoria})
        if r_cat.status_code == 200 and r_cat.json():
            params["category"] = r_cat.json()[0]["id"]

    r = await client.get("/wp-json/wc/v3/products", params=params)
    if r.status_code != 200:
        return {"errore": f"HTTP {r.status_code}"}

    prodotti = [
        {
            "id": p["id"],
            "nome": p["name"],
            "sku": p["sku"],
            "prezzo": p["regular_price"],
            "stock": p.get("stock_quantity", 0),
            "stato": p["status"],
        }
        for p in r.json()
    ]
    return {"totale": len(prodotti), "prodotti": prodotti}


async def _get_or_create_categoria(client: httpx.AsyncClient, nome: str) -> int | None:
    """Cerca una categoria WooCommerce per nome, la crea se non esiste."""
    r = await client.get("/wp-json/wc/v3/products/categories", params={"search": nome})
    if r.status_code == 200 and r.json():
        return r.json()[0]["id"]
    # Crea categoria
    r_create = await client.post("/wp-json/wc/v3/products/categories", json={"name": nome})
    if r_create.status_code in (200, 201):
        return r_create.json()["id"]
    return None


# ==========================================
# PAGINE WORDPRESS
# ==========================================

async def crea_pagina_html(
    titolo: str,
    contenuto_html: str,
    slug: str | None = None,
    stato: str = "draft",
) -> dict:
    """Crea una nuova pagina WordPress con contenuto HTML."""
    client = get_wp_client()
    contenuto_html = _ensure_accessible_html_contrast(contenuto_html)

    payload = {
        "title": titolo,
        "content": contenuto_html,
        "status": stato,
    }
    if slug:
        payload["slug"] = slug

    r = await client.post("/wp-json/wp/v2/pages", json=payload)
    if r.status_code in (200, 201):
        data = r.json()
        return {
            "successo": True,
            "id": data["id"],
            "titolo": data["title"]["rendered"],
            "url": data["link"],
            "stato": data["status"],
        }
    return {"errore": f"HTTP {r.status_code}: {r.text[:200]}"}


async def scrivi_pagina_html(
    page_id: int,
    contenuto_html: str,
    titolo: str | None = None,
    stato: str | None = None,
) -> dict:
    """Modifica il contenuto HTML di una pagina WordPress esistente."""
    client = get_wp_client()
    contenuto_html = _ensure_accessible_html_contrast(contenuto_html)

    payload = {"content": contenuto_html}
    if titolo:
        payload["title"] = titolo
    if stato:
        payload["status"] = stato

    r = await client.post(f"/wp-json/wp/v2/pages/{page_id}", json=payload)
    if r.status_code == 200:
        data = r.json()
        return {
            "successo": True,
            "id": data["id"],
            "titolo": data["title"]["rendered"],
            "url": data["link"],
        }
    return {"errore": f"HTTP {r.status_code}: {r.text[:200]}"}


async def leggi_pagina_html(page_id: int) -> dict:
    """Legge il contenuto HTML di una pagina WordPress."""
    client = get_wp_client()

    r = await client.get(f"/wp-json/wp/v2/pages/{page_id}")
    if r.status_code == 200:
        data = r.json()
        return {
            "id": data["id"],
            "titolo": data["title"]["rendered"],
            "contenuto": data["content"]["rendered"],
            "stato": data["status"],
            "url": data["link"],
        }
    return {"errore": f"HTTP {r.status_code}: {r.text[:200]}"}


async def ispeziona_pagina_elementor(page_id: int) -> dict:
    """Legge i metadati Elementor di una pagina."""
    client = get_wp_client()

    r = await client.get(
        f"/wp-json/wp/v2/pages/{page_id}",
        params={"context": "edit"},
    )
    if r.status_code != 200:
        return {"errore": f"HTTP {r.status_code}"}

    data = r.json()
    meta = data.get("meta", {})
    elementor_data = meta.get("_elementor_data", None)
    usa_elementor = bool(elementor_data)

    return {
        "id": data["id"],
        "titolo": data["title"]["raw"],
        "usa_elementor": usa_elementor,
        "elementor_data_presente": usa_elementor,
        "stato": data["status"],
        "url": data["link"],
    }


async def lista_pagine_elementor() -> dict:
    """Lista tutte le pagine distinguendo Elementor da HTML puro."""
    client = get_wp_client()

    r = await client.get("/wp-json/wp/v2/pages", params={"per_page": 100, "context": "edit"})
    if r.status_code != 200:
        return {"errore": f"HTTP {r.status_code}"}

    pagine = []
    for p in r.json():
        meta = p.get("meta", {})
        usa_elementor = bool(meta.get("_elementor_data"))
        pagine.append({
            "id": p["id"],
            "titolo": p["title"]["rendered"],
            "stato": p["status"],
            "url": p["link"],
            "tipo": "elementor" if usa_elementor else "html",
        })

    return {
        "totale": len(pagine),
        "elementor": [p for p in pagine if p["tipo"] == "elementor"],
        "html": [p for p in pagine if p["tipo"] == "html"],
    }


# ==========================================
# OPERAZIONI BULK E ATTRIBUTI
# ==========================================

async def importa_prodotti_bulk(prodotti: list) -> dict:
    """
    Importa una lista di prodotti in WooCommerce in batch da 5 in parallelo.

    Ogni elemento della lista deve avere: nome, prezzo, descrizione, sku.
    Campi opzionali: stock, categoria, attributi (dict).

    Ritorna un riepilogo con contatori e dettagli degli errori.
    """
    if not prodotti:
        return {"errore": "Lista prodotti vuota"}

    importati = []
    falliti = []
    batch_size = 5

    for i in range(0, len(prodotti), batch_size):
        batch = prodotti[i:i + batch_size]
        tasks = []
        for p in batch:
            attributi = p.pop("attributi", None)
            related_sku_code = p.pop("related_sku_code", None)
            if related_sku_code:
                p["related_sku_code"] = related_sku_code
            tasks.append(_crea_e_attributi(p, attributi))

        risultati = await asyncio.gather(*tasks, return_exceptions=True)
        for r in risultati:
            if isinstance(r, Exception) or (isinstance(r, dict) and r.get("errore")):
                falliti.append({"errore": str(r)} if isinstance(r, Exception) else r)
            else:
                importati.append(r)

    return {
        "importati": len(importati),
        "falliti": len(falliti),
        "dettagli_importati": importati,
        "dettagli_falliti": falliti,
    }


async def _crea_e_attributi(prodotto: dict, attributi: dict | None = None) -> dict:
    """Helper: crea prodotto e aggiunge attributi se presenti."""
    result = await crea_prodotto(**prodotto)
    if result.get("errore") or not attributi:
        return result
    attr_result = await aggiungi_attributi_prodotto(result["id"], attributi)
    result["attributi"] = attr_result
    return result


async def crea_struttura_categorie(categorie: list) -> dict:
    """
    Crea un albero di categorie WooCommerce in sequenza rispettando la gerarchia.

    Input:
      [
        {"nome": "Filtri", "parent": null},
        {"nome": "Filtri Olio", "parent": "Filtri"},
        {"nome": "Filtri Aria", "parent": "Filtri"},
      ]

    Ritorna mappa nome → id per uso successivo.
    """
    client = get_wp_client()
    mappa_id = {}  # nome → id

    for cat in categorie:
        nome = cat["nome"]
        parent_nome = cat.get("parent")
        parent_id = mappa_id.get(parent_nome, 0) if parent_nome else 0

        # Controlla se esiste già
        r = await client.get("/wp-json/wc/v3/products/categories", params={"search": nome})
        if r.status_code == 200:
            esistenti = [c for c in r.json() if c["name"].lower() == nome.lower()]
            if esistenti:
                mappa_id[nome] = esistenti[0]["id"]
                continue

        # Crea la categoria
        payload = {"name": nome, "parent": parent_id}
        r_create = await client.post("/wp-json/wc/v3/products/categories", json=payload)
        if r_create.status_code in (200, 201):
            mappa_id[nome] = r_create.json()["id"]
        else:
            mappa_id[nome] = None  # Fallita, continua

    create = {k: v for k, v in mappa_id.items() if v}
    fallite = [k for k, v in mappa_id.items() if not v]
    return {"create": create, "fallite": fallite, "totale": len(create)}


async def aggiungi_attributi_prodotto(product_id: int, attributi: dict) -> dict:
    """
    Aggiunge attributi a un prodotto WooCommerce esistente.

    attributi: dict con chiavi libere, es:
      {"marca_auto": "BMW", "modello": "Serie 3", "anno": "2005-2012", "codice_oe": "11427566327"}

    Gli attributi vengono aggiunti come attributi visibili sulla pagina prodotto.
    """
    client = get_wp_client()

    wc_attributes = [
        {"name": k, "options": [str(v)], "visible": True}
        for k, v in attributi.items()
    ]

    r = await client.put(
        f"/wp-json/wc/v3/products/{product_id}",
        json={"attributes": wc_attributes},
    )
    if r.status_code == 200:
        return {"successo": True, "product_id": product_id, "attributi_aggiunti": list(attributi.keys())}
    return {"errore": f"HTTP {r.status_code}: {r.text[:200]}"}


# ==========================================
# RICERCA PER RELATED_SKU_CODE
# ==========================================

async def cerca_prodotti_per_related_sku(related_sku_code: str) -> dict:
    """
    Cerca tutti i prodotti WooCommerce con un dato related_sku_code.
    Usa la WooCommerce REST API con filtro meta_data.
    Ritorna lista di prodotti con id, nome, sku, prezzo, descrizione.
    """
    client = get_wp_client()

    # WooCommerce non supporta filtro meta diretto via REST API standard
    # Recuperiamo tutti e filtriamo lato server (max 100 per pagina)
    tutti = []
    pagina = 1
    while True:
        r = await client.get("/wp-json/wc/v3/products", params={
            "per_page": 100,
            "page": pagina,
            "status": "any",
        })
        if r.status_code != 200:
            return {"errore": f"HTTP {r.status_code}"}
        batch = r.json()
        if not batch:
            break
        tutti.extend(batch)
        if len(batch) < 100:
            break
        pagina += 1

    # Filtra per related_sku_code nei meta_data
    trovati = []
    for p in tutti:
        meta = p.get("meta_data", [])
        for m in meta:
            if m.get("key") == "related_sku_code" and str(m.get("value", "")).lower() == related_sku_code.lower():
                trovati.append({
                    "id": p["id"],
                    "nome": p["name"],
                    "sku": p["sku"],
                    "prezzo": p["regular_price"],
                    "descrizione": p.get("description", "")[:200],
                    "related_sku_code": related_sku_code,
                })
                break

    return {
        "related_sku_code": related_sku_code,
        "trovati": len(trovati),
        "prodotti": trovati,
    }


# ==========================================
# AGGIORNAMENTO DESCRIZIONI IN BULK
# ==========================================

async def aggiorna_descrizioni_bulk(aggiornamenti: list) -> dict:
    """
    Aggiorna descrizione e/o nome di più prodotti in batch.

    aggiornamenti: lista di dict, ognuno con:
      - product_id: int (obbligatorio)
      - descrizione: str (opzionale)
      - nome: str (opzionale)

    Usa la WooCommerce batch API per efficienza.
    """
    client = get_wp_client()

    if not aggiornamenti:
        return {"errore": "Lista aggiornamenti vuota"}

    update_payload = []
    for a in aggiornamenti:
        item = {"id": a["product_id"]}
        if "descrizione" in a:
            item["description"] = a["descrizione"]
        if "nome" in a:
            item["name"] = a["nome"]
        update_payload.append(item)

    # WooCommerce batch API: max 100 per batch
    aggiornati = 0
    errori = []
    for i in range(0, len(update_payload), 100):
        batch = update_payload[i:i + 100]
        r = await client.post("/wp-json/wc/v3/products/batch", json={"update": batch})
        if r.status_code == 200:
            data = r.json()
            aggiornati += len(data.get("update", []))
        else:
            errori.append(f"Batch {i//100}: HTTP {r.status_code}")

    return {
        "successo": True,
        "aggiornati": aggiornati,
        "totale_richiesti": len(aggiornamenti),
        "errori": errori if errori else None,
    }


# ==========================================
# AGGIORNAMENTO PREZZI IN BULK
# ==========================================

async def aggiorna_prezzi_bulk(aggiornamenti: list) -> dict:
    """
    Aggiorna prezzi di più prodotti in batch.

    aggiornamenti: lista di dict, ognuno con:
      - product_id: int
      - prezzo: float (regular_price)
      - prezzo_scontato: float (opzionale, sale_price)

    Usa la WooCommerce batch API.
    """
    client = get_wp_client()

    if not aggiornamenti:
        return {"errore": "Lista aggiornamenti vuota"}

    update_payload = []
    for a in aggiornamenti:
        item = {"id": a["product_id"], "regular_price": str(a["prezzo"])}
        if "prezzo_scontato" in a and a["prezzo_scontato"] is not None:
            item["sale_price"] = str(a["prezzo_scontato"])
        update_payload.append(item)

    aggiornati = 0
    errori = []
    for i in range(0, len(update_payload), 100):
        batch = update_payload[i:i + 100]
        r = await client.post("/wp-json/wc/v3/products/batch", json={"update": batch})
        if r.status_code == 200:
            data = r.json()
            aggiornati += len(data.get("update", []))
        else:
            errori.append(f"Batch {i//100}: HTTP {r.status_code}")

    return {
        "successo": True,
        "aggiornati": aggiornati,
        "totale_richiesti": len(aggiornamenti),
        "errori": errori if errori else None,
    }


# ==========================================
# MODIFICA PRODOTTO ESTESA (meta_data, sku, immagini)
# ==========================================

async def modifica_prodotto_completo(
    product_id: int,
    nome: str | None = None,
    prezzo: float | None = None,
    prezzo_scontato: float | None = None,
    descrizione: str | None = None,
    descrizione_breve: str | None = None,
    stock: int | None = None,
    sku: str | None = None,
    meta_data: dict | None = None,
    immagini: list | None = None,
) -> dict:
    """
    Modifica completa di un prodotto WooCommerce.
    Supporta tutti i campi inclusi meta_data, immagini e SKU.

    meta_data: dict chiave-valore (es: {"related_sku_code": "R304"})
    immagini: lista di URL (es: ["https://example.com/img.jpg"])
    """
    client = get_wp_client()

    payload = {}
    if nome is not None:
        payload["name"] = nome
    if prezzo is not None:
        payload["regular_price"] = str(prezzo)
    if prezzo_scontato is not None:
        payload["sale_price"] = str(prezzo_scontato)
    if descrizione is not None:
        payload["description"] = descrizione
    if descrizione_breve is not None:
        payload["short_description"] = descrizione_breve
    if stock is not None:
        payload["stock_quantity"] = stock
        payload["manage_stock"] = True
    if sku is not None:
        payload["sku"] = sku
    if meta_data:
        payload["meta_data"] = [{"key": k, "value": v} for k, v in meta_data.items()]
    if immagini:
        payload["images"] = [{"src": url} for url in immagini]

    r = await client.put(f"/wp-json/wc/v3/products/{product_id}", json=payload)
    if r.status_code == 200:
        data = r.json()
        return {
            "successo": True,
            "id": data["id"],
            "nome": data["name"],
            "prezzo": data["regular_price"],
            "sku": data.get("sku", ""),
        }
    return {"errore": f"HTTP {r.status_code}: {r.text[:200]}"}


# ==========================================
# POST BLOG WORDPRESS
# ==========================================

async def crea_post_blog(
    titolo: str,
    contenuto_html: str,
    slug: str | None = None,
    stato: str = "draft",
    categoria: str | None = None,
    tags: list | None = None,
    excerpt: str | None = None,
    immagine_copertina: str | None = None,
) -> dict:
    """
    Crea un post blog WordPress via /wp-json/wp/v2/posts.
    Diverso da crea_pagina_html che crea pagine statiche.

    Se categoria non è specificata, l'agente prova ad assegnarla automaticamente
    usando le regole salvate nel contesto sito.
    """
    client = get_wp_client()
    contenuto_html = _ensure_accessible_html_contrast(contenuto_html)

    categoria_assegnata = categoria or _infer_blog_category(
        titolo=titolo,
        contenuto_html=contenuto_html,
        excerpt=excerpt,
        tags=tags,
    )

    payload = {
        "title": titolo,
        "content": contenuto_html,
        "status": stato,
    }
    if slug:
        payload["slug"] = slug
    if excerpt:
        payload["excerpt"] = excerpt

    if categoria_assegnata:
        cat_id = await _get_or_create_blog_categoria(client, categoria_assegnata)
        if cat_id:
            payload["categories"] = [cat_id]

    if tags:
        tag_ids = []
        for tag_nome in tags:
            tag_id = await _get_or_create_tag(client, tag_nome)
            if tag_id:
                tag_ids.append(tag_id)
        if tag_ids:
            payload["tags"] = tag_ids

    if immagine_copertina:
        media_id = await _upload_immagine_da_url(client, immagine_copertina)
        if media_id:
            payload["featured_media"] = media_id

    r = await client.post("/wp-json/wp/v2/posts", json=payload)
    if r.status_code in (200, 201):
        data = r.json()
        return {
            "successo": True,
            "id": data["id"],
            "titolo": data["title"]["rendered"],
            "url": data["link"],
            "stato": data["status"],
            "categoria_assegnata": categoria_assegnata,
            "categoria_automatica": categoria is None and bool(categoria_assegnata),
        }
    return {"errore": f"HTTP {r.status_code}: {r.text[:200]}"}


async def modifica_post_blog(
    post_id: int,
    titolo: str | None = None,
    contenuto_html: str | None = None,
    stato: str | None = None,
    excerpt: str | None = None,
    categoria: str | None = None,
    tags: list | None = None,
) -> dict:
    """Modifica un post blog esistente, con supporto opzionale per categorie e tag."""
    client = get_wp_client()

    payload = {}
    if titolo:
        payload["title"] = titolo
    if contenuto_html:
        payload["content"] = _ensure_accessible_html_contrast(contenuto_html)
    if stato:
        payload["status"] = stato
    if excerpt:
        payload["excerpt"] = excerpt
    if categoria:
        cat_id = await _get_or_create_blog_categoria(client, categoria)
        if cat_id:
            payload["categories"] = [cat_id]
    if tags is not None:
        tag_ids = []
        for tag_nome in tags:
            tag_id = await _get_or_create_tag(client, tag_nome)
            if tag_id:
                tag_ids.append(tag_id)
        payload["tags"] = tag_ids

    r = await client.post(f"/wp-json/wp/v2/posts/{post_id}", json=payload)
    if r.status_code == 200:
        data = r.json()
        return {
            "successo": True,
            "id": data["id"],
            "titolo": data["title"]["rendered"],
            "url": data["link"],
            "categoria_assegnata": categoria,
        }
    return {"errore": f"HTTP {r.status_code}: {r.text[:200]}"}


async def lista_post_blog(search: str = None, categoria: str = None, limit: int = 20) -> dict:
    """Lista post blog con filtri opzionali."""
    client = get_wp_client()

    params = {"per_page": min(limit, 100)}
    if search:
        params["search"] = search
    if categoria:
        r_cat = await client.get("/wp-json/wp/v2/categories", params={"search": categoria})
        if r_cat.status_code == 200 and r_cat.json():
            params["categories"] = r_cat.json()[0]["id"]

    r = await client.get("/wp-json/wp/v2/posts", params=params)
    if r.status_code != 200:
        return {"errore": f"HTTP {r.status_code}"}

    posts = [
        {
            "id": p["id"],
            "titolo": p["title"]["rendered"],
            "stato": p["status"],
            "data": p["date"][:10],
            "url": p["link"],
        }
        for p in r.json()
    ]
    return {"totale": len(posts), "posts": posts}


async def aggiungi_voce_menu(
    titolo: str,
    url: str,
    menu_location: str | None = "primary",
    menu_slug: str | None = None,
    menu_id: int | None = None,
    parent_id: int = 0,
    menu_order: int | None = None,
    object_id: int | None = None,
    object_type: str = "page",
    item_type: str | None = None,
) -> dict:
    """Aggiunge una voce a un menu WordPress, evitando duplicati nello stesso menu."""
    client = get_wp_client()

    resolved_menu_id = await _resolve_menu_id(
        client,
        menu_id=menu_id,
        menu_slug=menu_slug,
        menu_location=menu_location,
    )
    if not resolved_menu_id:
        return {"errore": "Menu non trovato"}

    items_resp = await client.get(
        "/wp-json/wp/v2/menu-items",
        params={"menus": resolved_menu_id, "per_page": 100, "context": "edit"},
    )
    if items_resp.status_code != 200:
        return {"errore": f"HTTP {items_resp.status_code}: {items_resp.text[:200]}"}

    items = items_resp.json()
    titolo_norm = _normalize_text(titolo)
    url_norm = url.rstrip("/")
    for item in items:
        item_title = _normalize_text(item.get("title", {}).get("rendered", ""))
        item_url = (item.get("url") or "").rstrip("/")
        if item_title == titolo_norm or item_url == url_norm:
            return {
                "successo": True,
                "esistente": True,
                "menu_id": resolved_menu_id,
                "item_id": item.get("id"),
                "titolo": item.get("title", {}).get("rendered", titolo),
                "url": item.get("url"),
            }

    next_order = menu_order or (max((item.get("menu_order", 0) for item in items), default=0) + 1)
    payload = {
        "title": titolo,
        "status": "publish",
        "menus": resolved_menu_id,
        "parent": parent_id,
        "menu_order": next_order,
    }
    if object_id:
        payload.update({
            "type": item_type or "post_type",
            "object": object_type,
            "object_id": object_id,
        })
    else:
        payload.update({
            "type": item_type or "custom",
            "object": "custom",
            "url": url,
        })

    r = await client.post("/wp-json/wp/v2/menu-items", json=payload)
    if r.status_code not in (200, 201):
        return {"errore": f"HTTP {r.status_code}: {r.text[:200]}"}

    data = r.json()
    aggiorna_contesto_sito("blog_menu_principale", f"{titolo} -> {data.get('url', url)}")
    return {
        "successo": True,
        "esistente": False,
        "menu_id": resolved_menu_id,
        "item_id": data.get("id"),
        "titolo": data.get("title", {}).get("rendered", titolo),
        "url": data.get("url", url),
        "menu_order": data.get("menu_order", next_order),
    }


async def imposta_regola_categorie_blog(regole: dict | None = None, attiva: bool = True) -> dict:
    """Salva le regole automatiche di categoria per i futuri articoli creati dall'agente."""
    regole_finali = DEFAULT_BLOG_CATEGORY_RULES.copy()
    if regole:
        for categoria, keyword_list in regole.items():
            pulite = [str(keyword).strip() for keyword in keyword_list if str(keyword).strip()]
            if pulite:
                regole_finali[categoria] = pulite

    aggiorna_contesto_sito("blog_regole_categorie", json.dumps(regole_finali, ensure_ascii=False))
    aggiorna_contesto_sito("blog_regole_categorie_attive", "true" if attiva else "false")
    return {
        "successo": True,
        "attiva": attiva,
        "categorie": sorted(regole_finali.keys()),
        "regole": regole_finali,
    }


async def leggi_impostazioni_wordpress() -> dict:
    """Legge le impostazioni principali del sito WordPress utili all'agente."""
    client = get_wp_client()

    r = await client.get("/wp-json/wp/v2/settings")
    if r.status_code != 200:
        return {"errore": f"HTTP {r.status_code}: {r.text[:200]}"}

    data = r.json()
    return {
        "successo": True,
        "titolo_sito": data.get("title"),
        "descrizione": data.get("description"),
        "url": data.get("url"),
        "show_on_front": data.get("show_on_front"),
        "page_on_front": data.get("page_on_front"),
        "page_for_posts": data.get("page_for_posts"),
        "default_category": data.get("default_category"),
        "posts_per_page": data.get("posts_per_page"),
        "default_comment_status": data.get("default_comment_status"),
    }


async def ispeziona_struttura_blog() -> dict:
    """Ispeziona pagina blog, categorie e post per capire la struttura reale del blog."""
    client = get_wp_client()

    settings_resp = await client.get("/wp-json/wp/v2/settings")
    if settings_resp.status_code != 200:
        return {"errore": f"HTTP {settings_resp.status_code}: {settings_resp.text[:200]}"}
    settings = settings_resp.json()

    page_for_posts = settings.get("page_for_posts")
    page_on_front = settings.get("page_on_front")

    blog_page = None
    if page_for_posts:
        r_page = await client.get(f"/wp-json/wp/v2/pages/{page_for_posts}")
        if r_page.status_code == 200:
            p = r_page.json()
            blog_page = {
                "id": p["id"],
                "titolo": p["title"]["rendered"],
                "slug": p.get("slug"),
                "url": p.get("link"),
                "stato": p.get("status"),
            }

    categorie = await lista_categorie_blog(limit=100)
    posts = await lista_post_blog(limit=50)

    senza_categoria = []
    categorie_trovate = []
    if posts.get("posts"):
        r_posts = await client.get("/wp-json/wp/v2/posts", params={"per_page": 50, "_embed": 1})
        if r_posts.status_code == 200:
            for post in r_posts.json():
                cats = post.get("categories", [])
                if not cats or 1 in cats:
                    senza_categoria.append({
                        "id": post["id"],
                        "titolo": post["title"]["rendered"],
                        "url": post["link"],
                    })
        categorie_trovate = categorie.get("categorie", [])

    categorie_utili = [
        "Guide Ricambi",
        "Manutenzione Auto",
        "Problemi e Diagnosi",
        "Confronti e Recensioni",
        "News Auto Elettriche",
    ]
    nomi_esistenti = {c["nome"].lower() for c in categorie_trovate}
    categorie_mancanti = [nome for nome in categorie_utili if nome.lower() not in nomi_esistenti]

    return {
        "successo": True,
        "settings": {
            "show_on_front": settings.get("show_on_front"),
            "page_on_front": page_on_front,
            "page_for_posts": page_for_posts,
            "posts_per_page": settings.get("posts_per_page"),
        },
        "pagina_blog": blog_page,
        "categorie_totali": categorie.get("totale", 0),
        "categorie": categorie_trovate,
        "post_totali": posts.get("totale", 0),
        "post_senza_categoria_utile": senza_categoria,
        "categorie_consigliate_mancanti": categorie_mancanti,
    }


async def crea_struttura_blog_completa(categorie: list[str] | None = None) -> dict:
    """
    Crea la struttura base del blog Auto-Volt: categorie principali e salvataggio contesto.
    Non tocca i post esistenti, non pubblica articoli e non modifica la page_for_posts.
    """
    default_categorie = categorie or [
        "Guide Ricambi",
        "Manutenzione Auto",
        "Problemi e Diagnosi",
        "Confronti e Recensioni",
        "News Auto Elettriche",
    ]

    creati = []
    esistenti = []
    errori = []

    for nome in default_categorie:
        result = await crea_categoria_blog(nome=nome)
        if result.get("errore"):
            errori.append({"nome": nome, "errore": result["errore"]})
            continue
        item = {
            "id": result.get("id"),
            "nome": result.get("nome", nome),
            "slug": result.get("slug"),
        }
        if result.get("esistente"):
            esistenti.append(item)
        else:
            creati.append(item)

    struttura = [c["nome"] for c in creati + esistenti]
    aggiorna_contesto_sito("blog_struttura_categorie", ", ".join(struttura))
    aggiorna_contesto_sito("blog_preferenza", "Organizzare i post del blog in categorie stabili e riusabili")

    ispezione = await ispeziona_struttura_blog()

    return {
        "successo": len(errori) == 0,
        "categorie_create": creati,
        "categorie_esistenti": esistenti,
        "errori": errori,
        "ispezione": ispezione,
    }


async def crea_categoria_blog(
    nome: str,
    slug: str | None = None,
    descrizione: str | None = None,
    parent_id: int | None = None,
) -> dict:
    """Crea una categoria blog WordPress esplicita, se non esiste già."""
    client = get_wp_client()

    r = await client.get("/wp-json/wp/v2/categories", params={"search": nome, "per_page": 100})
    if r.status_code == 200:
        for c in r.json():
            if c["name"].lower() == nome.lower() or (slug and c.get("slug") == slug):
                return {
                    "successo": True,
                    "esistente": True,
                    "id": c["id"],
                    "nome": c["name"],
                    "slug": c.get("slug"),
                    "parent": c.get("parent", 0),
                }

    payload = {"name": nome}
    if slug:
        payload["slug"] = slug
    if descrizione:
        payload["description"] = descrizione
    if parent_id:
        payload["parent"] = parent_id

    r = await client.post("/wp-json/wp/v2/categories", json=payload)
    if r.status_code in (200, 201):
        data = r.json()
        return {
            "successo": True,
            "esistente": False,
            "id": data["id"],
            "nome": data["name"],
            "slug": data.get("slug"),
            "parent": data.get("parent", 0),
        }
    return {"errore": f"HTTP {r.status_code}: {r.text[:200]}"}


async def lista_categorie_blog(search: str | None = None, limit: int = 50) -> dict:
    """Lista categorie blog WordPress."""
    client = get_wp_client()

    params = {"per_page": min(limit, 100)}
    if search:
        params["search"] = search

    r = await client.get("/wp-json/wp/v2/categories", params=params)
    if r.status_code != 200:
        return {"errore": f"HTTP {r.status_code}: {r.text[:200]}"}

    categorie = [
        {
            "id": c["id"],
            "nome": c["name"],
            "slug": c.get("slug"),
            "parent": c.get("parent", 0),
            "descrizione": c.get("description", ""),
            "conteggio_post": c.get("count", 0),
        }
        for c in r.json()
    ]
    return {"totale": len(categorie), "categorie": categorie}


# ==========================================
# HELPER: Categorie blog, menu, tag, immagini
# ==========================================

def _normalize_text(value: str | None) -> str:
    if not value:
        return ""
    normalized = unicodedata.normalize("NFKD", value)
    ascii_only = normalized.encode("ascii", "ignore").decode("ascii")
    return re.sub(r"\s+", " ", ascii_only).strip().lower()


def _load_blog_category_rules() -> dict[str, list[str]]:
    stored = leggi_contesto_sito("blog_regole_categorie")
    raw_value = stored.get("valore") if stored.get("chiave") == "blog_regole_categorie" else None
    if raw_value:
        try:
            parsed = json.loads(raw_value)
            if isinstance(parsed, dict):
                return {key: [str(item) for item in value] for key, value in parsed.items() if isinstance(value, list)}
        except json.JSONDecodeError:
            pass
    return DEFAULT_BLOG_CATEGORY_RULES


def _blog_category_rules_enabled() -> bool:
    stored = leggi_contesto_sito("blog_regole_categorie_attive")
    raw_value = stored.get("valore") if stored.get("chiave") == "blog_regole_categorie_attive" else None
    if raw_value is None:
        return True
    return str(raw_value).strip().lower() == "true"


def _infer_blog_category(
    titolo: str,
    contenuto_html: str | None = None,
    excerpt: str | None = None,
    tags: list[str] | None = None,
) -> str:
    if not _blog_category_rules_enabled():
        return "Guide Ricambi"

    combined = " ".join(filter(None, [titolo, excerpt, contenuto_html or "", " ".join(tags or [])]))
    normalized = _normalize_text(combined)
    best_category = "Guide Ricambi"
    best_score = 0

    for category, keywords in _load_blog_category_rules().items():
        score = sum(1 for keyword in keywords if _normalize_text(keyword) in normalized)
        if score > best_score:
            best_category = category
            best_score = score

    return best_category


async def _resolve_menu_id(
    client,
    menu_id: int | None = None,
    menu_slug: str | None = None,
    menu_location: str | None = None,
) -> int | None:
    if menu_id:
        return menu_id

    if menu_location:
        r_location = await client.get(f"/wp-json/wp/v2/menu-locations/{menu_location}")
        if r_location.status_code == 200:
            location = r_location.json()
            if location.get("menu"):
                return location["menu"]

    if menu_slug:
        r_menus = await client.get("/wp-json/wp/v2/menus", params={"per_page": 100})
        if r_menus.status_code == 200:
            for menu in r_menus.json():
                if menu.get("slug") == menu_slug or _normalize_text(menu.get("name")) == _normalize_text(menu_slug):
                    return menu.get("id")

    return None


async def _get_or_create_blog_categoria(client, nome: str) -> int | None:
    """Cerca o crea una categoria blog WordPress (diversa da WooCommerce)."""
    r = await client.get("/wp-json/wp/v2/categories", params={"search": nome})
    if r.status_code == 200 and r.json():
        for c in r.json():
            if c["name"].lower() == nome.lower():
                return c["id"]
    r_create = await client.post("/wp-json/wp/v2/categories", json={"name": nome})
    if r_create.status_code in (200, 201):
        return r_create.json()["id"]
    return None


async def _get_or_create_tag(client, nome: str) -> int | None:
    """Cerca o crea un tag WordPress."""
    r = await client.get("/wp-json/wp/v2/tags", params={"search": nome})
    if r.status_code == 200 and r.json():
        for t in r.json():
            if t["name"].lower() == nome.lower():
                return t["id"]
    r_create = await client.post("/wp-json/wp/v2/tags", json={"name": nome})
    if r_create.status_code in (200, 201):
        return r_create.json()["id"]
    return None


async def _upload_immagine_da_url(client, url: str) -> int | None:
    """Scarica un'immagine da URL e la carica nella media library WordPress."""
    try:
        import httpx as _httpx
        async with _httpx.AsyncClient(follow_redirects=True) as dl:
            resp = await dl.get(url, timeout=30)
            if resp.status_code != 200:
                return None
            content = resp.content
            content_type = resp.headers.get("content-type", "image/jpeg")

        # Estrai nome file dall'URL
        filename = url.split("/")[-1].split("?")[0]
        if not filename or "." not in filename:
            filename = "immagine.jpg"

        r = await client.post(
            "/wp-json/wp/v2/media",
            content=content,
            headers={
                "Content-Type": content_type,
                "Content-Disposition": f'attachment; filename="{filename}"',
            },
        )
        if r.status_code in (200, 201):
            return r.json()["id"]
    except Exception:
        pass
    return None
