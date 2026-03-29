"""Tool di analisi struttura pagina e scraping strutturato con Playwright."""
from collections import Counter

import httpx
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright

from config import Config


async def analizza_struttura_pagina(url: str) -> dict:
    """Analizza rapidamente l'HTML della pagina per trovare selettori candidati."""
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0 Safari/537.36"
    }

    async with httpx.AsyncClient(follow_redirects=True, timeout=30, headers=headers) as client:
        response = await client.get(url)

    if response.status_code != 200:
        return {"errore": f"HTTP {response.status_code}: {response.text[:200]}"}

    soup = BeautifulSoup(response.text, "html.parser")
    title = soup.title.get_text(" ", strip=True) if soup.title else ""
    h1 = [el.get_text(" ", strip=True) for el in soup.select("h1")[:5]]
    text = soup.get_text(" ", strip=True)

    selettori_base = (
        "article",
        ".post",
        ".post-card",
        ".blog-card",
        ".card",
        ".product",
        ".product-card",
        ".item",
        ".listing-item",
        "li",
        "tr",
    )
    selettori_candidati = []
    for selector in selettori_base:
        found = soup.select(selector)
        if found:
            selettori_candidati.append({
                "selector": selector,
                "count": len(found),
                "sample_text": found[0].get_text(" ", strip=True)[:160],
            })

    blocchi = Counter()
    for el in soup.find_all(["article", "div", "section", "li"]):
        classes = tuple(sorted(c for c in el.get("class", []) if c))
        if classes:
            blocchi[(el.name, classes)] += 1

    blocchi_ricorrenti = []
    for (tag, classes), count in blocchi.most_common(8):
        if count < 3:
            continue
        blocchi_ricorrenti.append({
            "selector": f"{tag}." + ".".join(classes[:2]),
            "count": count,
        })

    dinamica_probabile = len(text) < 400 and len(soup.find_all("script")) > 8
    strategia = "browser-use"
    if selettori_candidati or blocchi_ricorrenti:
        strategia = "playwright" if dinamica_probabile else "html-or-playwright"

    return {
        "successo": True,
        "url": str(response.url),
        "title": title,
        "h1": h1,
        "conteggio": {
            "link": len(soup.find_all("a")),
            "form": len(soup.find_all("form")),
            "table": len(soup.find_all("table")),
            "article": len(soup.find_all("article")),
            "script": len(soup.find_all("script")),
        },
        "selettori_candidati": selettori_candidati[:10],
        "blocchi_ricorrenti": blocchi_ricorrenti,
        "dinamica_probabile": dinamica_probabile,
        "strategia_consigliata": strategia,
        "consiglio": (
            "Esplora con browser-use se devi capire il flusso visivo, poi usa Playwright per estrazione precisa e ripetibile."
            if strategia in ("playwright", "html-or-playwright")
            else "La pagina sembra poco strutturata: usa browser-use per esplorare prima di estrarre dati."
        ),
    }


async def estrai_dati_con_playwright(
    url: str,
    selettori: list[str] | None = None,
    limite: int = 20,
    attesa_ms: int = 1500,
) -> dict:
    """Estrae dati testuali e link da una pagina renderizzata con Playwright."""
    selectors = selettori or [
        "article",
        ".post",
        ".blog-card",
        ".card",
        ".product",
        ".product-card",
        ".listing-item",
        "li",
        "tr",
    ]

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=Config.BROWSER_HEADLESS)
        page = await browser.new_page()
        await page.goto(url, wait_until="domcontentloaded", timeout=60000)
        await page.wait_for_timeout(attesa_ms)

        selector_usato = None
        total = 0
        for selector in selectors:
            try:
                current_total = await page.locator(selector).count()
            except Exception:
                current_total = 0
            if current_total > 0:
                selector_usato = selector
                total = current_total
                break

        if not selector_usato:
            preview = await page.locator("body").inner_text()
            title = await page.title()
            await browser.close()
            return {
                "successo": False,
                "url": url,
                "title": title,
                "errore": "Nessun selettore corrispondente trovato.",
                "preview": preview[:500],
            }

        elements = page.locator(selector_usato)
        data = []
        for idx in range(min(total, limite)):
            el = elements.nth(idx)
            try:
                text = (await el.inner_text()).strip()
            except Exception:
                text = ""
            href = None
            try:
                href = await el.locator("a").first.get_attribute("href")
            except Exception:
                href = None
            data.append({"index": idx, "text": text[:1200], "href": href})

        title = await page.title()
        await browser.close()
        return {
            "successo": True,
            "url": url,
            "title": title,
            "selettore_usato": selector_usato,
            "totale_elementi": total,
            "elementi": data,
        }