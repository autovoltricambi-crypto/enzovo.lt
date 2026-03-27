"""Operazioni WordPress/WooCommerce via REST API."""
import json
import httpx
from tools.cataloghi import get_wp_client


# ==========================================
# PRODOTTI WOOCOMMERCE
# ==========================================

async def crea_prodotto(
    nome: str,
    prezzo: float,
    descrizione: str,
    sku: str,
    stock: int = 0,
    categoria: str = None,
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

    if categoria:
        # Cerca o crea la categoria
        cat_id = await _get_or_create_categoria(client, categoria)
        if cat_id:
            payload["categories"] = [{"id": cat_id}]

    r = await client.post("/wp-json/wc/v3/products", json=payload)
    if r.status_code in (200, 201):
        data = r.json()
        return {
            "successo": True,
            "id": data["id"],
            "nome": data["name"],
            "prezzo": data["regular_price"],
            "sku": data["sku"],
        }
    return {"errore": f"HTTP {r.status_code}: {r.text[:200]}"}


async def modifica_prodotto(
    product_id: int,
    nome: str = None,
    prezzo: float = None,
    descrizione: str = None,
    stock: int = None,
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
    search: str = None,
    categoria: str = None,
    limit: int = 100,
) -> dict:
    """Elenca prodotti WooCommerce con filtri opzionali."""
    client = get_wp_client()

    params = {"per_page": min(limit, 100)}
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
    slug: str = None,
    stato: str = "draft",
) -> dict:
    """Crea una nuova pagina WordPress con contenuto HTML."""
    client = get_wp_client()

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
    titolo: str = None,
    stato: str = None,
) -> dict:
    """Modifica il contenuto HTML di una pagina WordPress esistente."""
    client = get_wp_client()

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
