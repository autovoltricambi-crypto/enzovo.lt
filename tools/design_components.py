"""Libreria componenti premium, template pagina e review HTML per AutoVolt."""

from __future__ import annotations

import html
import re
from typing import Any


PAGE_TEMPLATES = {
    "home": "Homepage commerciale con hero, fiducia, prove e CTA.",
    "landing": "Landing focalizzata su una singola offerta o servizio.",
    "category": "Pagina categoria con intro SEO, benefici, griglia e FAQ.",
    "product": "Scheda prodotto/descrizione lunga con prezzo, trust, FAQ e cross-sell.",
}


COMPONENT_LIBRARY = [
    {
        "tipo": "hero",
        "descrizione": "Sezione above-the-fold con promessa, sottotitolo e CTA.",
        "campi": ["badge", "titolo", "sottotitolo", "cta_primaria_testo", "cta_primaria_url"],
    },
    {
        "tipo": "trust_strip",
        "descrizione": "Barra orizzontale con elementi fiducia come spedizione, reso e supporto.",
        "campi": ["items"],
    },
    {
        "tipo": "stats",
        "descrizione": "Statistiche o numeri prova sociale in evidenza.",
        "campi": ["items"],
    },
    {
        "tipo": "feature_grid",
        "descrizione": "Griglia di card per benefici, servizi o sottocategorie.",
        "campi": ["titolo", "items"],
    },
    {
        "tipo": "split_section",
        "descrizione": "Sezione due colonne con testo e media/riquadro informativo.",
        "campi": ["titolo", "testo", "image_url"],
    },
    {
        "tipo": "price_box",
        "descrizione": "Box prezzo con recensioni, CTA e chip di rassicurazione.",
        "campi": ["prezzo", "prezzo_note", "review_label", "cta_primaria_testo", "cta_primaria_url"],
    },
    {
        "tipo": "testimonials",
        "descrizione": "Recensioni/testimonianze in card per riprova sociale.",
        "campi": ["titolo", "items"],
    },
    {
        "tipo": "faq",
        "descrizione": "Blocco FAQ in formato domanda/risposta.",
        "campi": ["titolo", "items"],
    },
    {
        "tipo": "cta_band",
        "descrizione": "Sezione finale di conversione con CTA primaria e secondaria.",
        "campi": ["titolo", "testo", "cta_primaria_testo", "cta_primaria_url"],
    },
    {
        "tipo": "product_cards",
        "descrizione": "Griglia di prodotti correlati o offerte secondarie.",
        "campi": ["titolo", "items"],
    },
    {
        "tipo": "checklist",
        "descrizione": "Lista benefici con checkmark.",
        "campi": ["titolo", "items"],
    },
    {
        "tipo": "logo_cloud",
        "descrizione": "Cloud di marchi, partner o certificazioni.",
        "campi": ["titolo", "items"],
    },
]


def _escape(value: Any) -> str:
    return html.escape(str(value or ""), quote=True)


def _strip_tags(value: str) -> str:
    return re.sub(r"<[^>]+>", "", value or "")


def _items(items: Any) -> list:
    if items is None:
        return []
    if isinstance(items, list):
        return [item for item in items if item not in (None, "")]
    return [items]


def _render_button(label: str | None, url: str | None, secondary: bool = False) -> str:
    if not label or not url:
        return ""
    classes = "av-cta av-cta-secondary" if secondary else "av-cta"
    return f'<a class="{classes}" href="{_escape(url)}">{_escape(label)}</a>'


def _render_chip_row(items: list[str]) -> str:
    chips = "".join(f'<span class="av-chip">{_escape(item)}</span>' for item in items if item)
    if not chips:
        return ""
    return f'<div class="av-chip-row">{chips}</div>'


def _render_section_head(titolo: str | None = None, kicker: str | None = None, testo: str | None = None) -> str:
    parts = []
    if kicker:
        parts.append(f'<p class="av-kicker">{_escape(kicker)}</p>')
    if titolo:
        parts.append(f"<h2>{_escape(titolo)}</h2>")
    if testo:
        parts.append(f"<p>{_escape(testo)}</p>")
    return "".join(parts)


def _render_hero(data: dict) -> str:
    actions = "".join(
        [
            _render_button(data.get("cta_primaria_testo"), data.get("cta_primaria_url")),
            _render_button(data.get("cta_secondaria_testo"), data.get("cta_secondaria_url"), secondary=True),
        ]
    )
    chips = _render_chip_row(_items(data.get("trust_items"))[:4])
    return (
        "<section class=\"av-hero\">"
        f"<span class=\"av-badge\">{_escape(data.get('badge') or 'AutoVolt')}</span>"
        f"<h1>{_escape(data.get('titolo') or '')}</h1>"
        f"<p>{_escape(data.get('sottotitolo') or '')}</p>"
        f"<div class=\"av-actions\">{actions}</div>"
        f"{chips}"
        "</section>"
    )


def _render_trust_strip(data: dict) -> str:
    items = _items(data.get("items"))
    body = "".join(f'<div class="av-trust-item">{_escape(item)}</div>' for item in items)
    if not body:
        return ""
    return f'<section class="av-trust-strip" aria-label="Elementi di fiducia">{body}</section>'


def _render_stats(data: dict) -> str:
    stats = []
    for item in _items(data.get("items")):
        if isinstance(item, dict):
            numero = item.get("numero") or item.get("value") or ""
            etichetta = item.get("etichetta") or item.get("label") or ""
        else:
            numero = item
            etichetta = ""
        stats.append(
            "<div class=\"av-stat\">"
            f"<span class=\"av-stat-num\">{_escape(numero)}</span>"
            f"<span class=\"av-stat-label\">{_escape(etichetta)}</span>"
            "</div>"
        )
    if not stats:
        return ""
    return f'<section><div class="av-stats">{"".join(stats)}</div></section>'


def _coerce_card_items(items: Any) -> list[dict]:
    result = []
    for item in _items(items):
        if isinstance(item, dict):
            result.append(item)
        else:
            result.append({"titolo": str(item), "testo": ""})
    return result


def _render_feature_grid(data: dict) -> str:
    cards = []
    for item in _coerce_card_items(data.get("items")):
        tag = f'<span class="av-badge">{_escape(item.get("tag"))}</span>' if item.get("tag") else ""
        cards.append(
            '<article class="av-card">'
            f"{tag}"
            f"<h3>{_escape(item.get('titolo') or item.get('title') or '')}</h3>"
            f"<p>{_escape(item.get('testo') or item.get('text') or '')}</p>"
            "</article>"
        )
    if not cards:
        return ""
    head = _render_section_head(data.get("titolo"), data.get("kicker"), data.get("testo"))
    return f'<section>{head}<div class="av-grid">{"".join(cards)}</div></section>'


def _render_checklist(data: dict) -> str:
    items = _items(data.get("items"))
    if not items:
        return ""
    list_html = "".join(f"<li>{_escape(item)}</li>" for item in items)
    head = _render_section_head(data.get("titolo"), data.get("kicker"), data.get("testo"))
    return f'<section>{head}<ul class="av-checklist">{list_html}</ul></section>'


def _render_split_section(data: dict) -> str:
    media = ""
    if data.get("image_url"):
        media = (
            '<div class="av-split-media">'
            f'<img src="{_escape(data.get("image_url"))}" alt="{_escape(data.get("image_alt") or data.get("titolo") or "AutoVolt")}" '
            'loading="lazy" decoding="async">'
            '</div>'
        )
    elif data.get("media_html"):
        media = f'<div class="av-split-media">{data.get("media_html")}</div>'
    else:
        media = (
            '<div class="av-split-media">'
            f'<div class="av-card"><h3>{_escape(data.get("media_title") or "Perche conta")}</h3>'
            f'<p>{_escape(data.get("media_text") or data.get("testo") or "")}</p></div>'
            '</div>'
        )
    copy = (
        '<div class="av-split-copy">'
        f'{_render_section_head(data.get("titolo"), data.get("kicker"), data.get("testo"))}'
        f'{_render_checklist({"items": data.get("benefici")}) if data.get("benefici") else ""}'
        f'<div class="av-actions">{_render_button(data.get("cta_primaria_testo"), data.get("cta_primaria_url"))}{_render_button(data.get("cta_secondaria_testo"), data.get("cta_secondaria_url"), secondary=True)}</div>'
        '</div>'
    )
    if data.get("reverse"):
        copy, media = media, copy
    return f'<section class="av-split">{copy}{media}</section>'


def _render_price_box(data: dict) -> str:
    trust = _render_chip_row(_items(data.get("trust_items")))
    reviews = ""
    if data.get("review_label"):
        reviews = f'<div class="av-review-row"><span class="av-review-stars">★★★★★</span><span>{_escape(data.get("review_label"))}</span></div>'
    return (
        '<section class="av-price-box">'
        f'{reviews}'
        f'<div class="av-price-value">{_escape(data.get("prezzo") or "")}</div>'
        f'<p class="av-price-note">{_escape(data.get("prezzo_note") or "IVA inclusa")}</p>'
        f'{trust}'
        f'<div class="av-actions">{_render_button(data.get("cta_primaria_testo"), data.get("cta_primaria_url"))}{_render_button(data.get("cta_secondaria_testo"), data.get("cta_secondaria_url"), secondary=True)}</div>'
        '</section>'
    )


def _render_testimonials(data: dict) -> str:
    cards = []
    for item in _coerce_card_items(data.get("items")):
        meta = ""
        if item.get("nome") or item.get("ruolo"):
            meta = f'<p class="av-testimonial-meta"><strong>{_escape(item.get("nome") or "")}</strong> { _escape(item.get("ruolo") or "") }</p>'
        cards.append(
            '<article class="av-testimonial av-card">'
            f'<p>"{_escape(item.get("testo") or item.get("text") or item.get("titolo") or "")}"</p>'
            f'{meta}'
            '</article>'
        )
    if not cards:
        return ""
    head = _render_section_head(data.get("titolo"), data.get("kicker"), data.get("testo"))
    return f'<section>{head}<div class="av-testimonials">{"".join(cards)}</div></section>'


def _render_faq(data: dict) -> str:
    items = []
    for item in _items(data.get("items")):
        if not isinstance(item, dict):
            continue
        items.append(f'<dt>{_escape(item.get("domanda") or item.get("question") or "")}</dt><dd>{_escape(item.get("risposta") or item.get("answer") or "")}</dd>')
    if not items:
        return ""
    head = _render_section_head(data.get("titolo") or "Domande frequenti", data.get("kicker"), data.get("testo"))
    return f'<section>{head}<dl>{"".join(items)}</dl></section>'


def _render_cta_band(data: dict) -> str:
    actions = (
        f'{_render_button(data.get("cta_primaria_testo"), data.get("cta_primaria_url"))}'
        f'{_render_button(data.get("cta_secondaria_testo"), data.get("cta_secondaria_url"), secondary=True)}'
    )
    return (
        '<section class="av-card av-cta-band">'
        f'{_render_section_head(data.get("titolo"), data.get("kicker"), data.get("testo"))}'
        f'<div class="av-actions">{actions}</div>'
        f'{_render_chip_row(_items(data.get("trust_items"))[:3])}'
        '</section>'
    )


def _render_product_cards(data: dict) -> str:
    cards = []
    for item in _coerce_card_items(data.get("items")):
        button = _render_button(item.get("cta_testo") or "Scopri di piu", item.get("url") or "#")
        cards.append(
            '<article class="av-card">'
            f'<h3>{_escape(item.get("titolo") or item.get("title") or "")}</h3>'
            f'<p>{_escape(item.get("testo") or item.get("text") or "")}</p>'
            f'{button}'
            '</article>'
        )
    if not cards:
        return ""
    head = _render_section_head(data.get("titolo"), data.get("kicker"), data.get("testo"))
    return f'<section>{head}<div class="av-grid">{"".join(cards)}</div></section>'


def _render_logo_cloud(data: dict) -> str:
    items = _items(data.get("items"))
    if not items:
        return ""
    logos = "".join(f'<div class="av-logo-item">{_escape(item if not isinstance(item, dict) else item.get("label") or item.get("nome") or "")}</div>' for item in items)
    head = _render_section_head(data.get("titolo"), data.get("kicker"), data.get("testo"))
    return f'<section>{head}<div class="av-logo-cloud">{logos}</div></section>'


def _render_component(component: dict) -> str:
    tipo = (component.get("tipo") or "").strip().lower()
    if tipo == "hero":
        return _render_hero(component)
    if tipo == "trust_strip":
        return _render_trust_strip(component)
    if tipo == "stats":
        return _render_stats(component)
    if tipo == "feature_grid":
        return _render_feature_grid(component)
    if tipo == "checklist":
        return _render_checklist(component)
    if tipo == "split_section":
        return _render_split_section(component)
    if tipo == "price_box":
        return _render_price_box(component)
    if tipo == "testimonials":
        return _render_testimonials(component)
    if tipo == "faq":
        return _render_faq(component)
    if tipo == "cta_band":
        return _render_cta_band(component)
    if tipo == "product_cards":
        return _render_product_cards(component)
    if tipo == "logo_cloud":
        return _render_logo_cloud(component)
    if tipo == "raw_html":
        return str(component.get("html") or "")
    raise ValueError(f"Componente non supportato: {tipo}")


def lista_componenti_premium() -> dict:
    return {
        "successo": True,
        "componenti": COMPONENT_LIBRARY,
        "template_supportati": PAGE_TEMPLATES,
        "workflow_consigliato": [
            "1. scegli il template pagina",
            "2. genera HTML da template o da componenti",
            "3. revisiona l'HTML con revisiona_html_premium",
            "4. se punteggio < 80, migliora e revisiona di nuovo",
            "5. solo dopo scrivi o pubblichi la pagina",
        ],
    }


def genera_blocchi_premium(componenti: list, titolo_pagina: str | None = None) -> dict:
    html_parts = []
    errori = []
    tipi = []
    for component in componenti or []:
        try:
            html_parts.append(_render_component(component))
            tipi.append(component.get("tipo"))
        except Exception as exc:
            errori.append(str(exc))

    result_html = "\n".join(part for part in html_parts if part)
    if titolo_pagina and "<h1" not in result_html.lower():
        result_html = f'<section class="av-hero"><h1>{_escape(titolo_pagina)}</h1></section>\n{result_html}'

    return {
        "successo": not errori,
        "html": result_html,
        "componenti_renderizzati": tipi,
        "errori": errori,
    }


def genera_template_pagina_premium(
    tipo_pagina: str,
    titolo: str,
    sottotitolo: str | None = None,
    badge: str | None = None,
    cta_primaria_testo: str | None = None,
    cta_primaria_url: str | None = None,
    cta_secondaria_testo: str | None = None,
    cta_secondaria_url: str | None = None,
    trust_items: list | None = None,
    benefici: list | None = None,
    cards: list | None = None,
    stats: list | None = None,
    faq: list | None = None,
    testimonials: list | None = None,
    prezzo: str | None = None,
    prezzo_note: str | None = None,
    review_label: str | None = None,
    image_url: str | None = None,
    image_alt: str | None = None,
    prodotti_correlati: list | None = None,
    intro_titolo: str | None = None,
    intro_testo: str | None = None,
) -> dict:
    tipo = (tipo_pagina or "").strip().lower()
    if tipo not in PAGE_TEMPLATES:
        return {"errore": f"tipo_pagina non supportato: {tipo_pagina}"}

    hero = {
        "tipo": "hero",
        "badge": badge or "AutoVolt",
        "titolo": titolo,
        "sottotitolo": sottotitolo or "",
        "cta_primaria_testo": cta_primaria_testo or "Contattaci",
        "cta_primaria_url": cta_primaria_url or "/contatti/",
        "cta_secondaria_testo": cta_secondaria_testo,
        "cta_secondaria_url": cta_secondaria_url,
        "trust_items": trust_items or [],
    }

    componenti = [hero]

    if tipo in {"home", "landing", "category"} and trust_items:
        componenti.append({"tipo": "trust_strip", "items": trust_items})

    if stats:
        componenti.append({"tipo": "stats", "items": stats})

    if tipo == "product" and prezzo:
        componenti.append(
            {
                "tipo": "price_box",
                "prezzo": prezzo,
                "prezzo_note": prezzo_note or "IVA inclusa - spedizione rapida disponibile",
                "review_label": review_label or "Supporto reale prima dell'acquisto",
                "cta_primaria_testo": cta_primaria_testo or "Aggiungi al carrello",
                "cta_primaria_url": cta_primaria_url or "#",
                "cta_secondaria_testo": cta_secondaria_testo,
                "cta_secondaria_url": cta_secondaria_url,
                "trust_items": trust_items or [],
            }
        )

    if benefici:
        if tipo == "product":
            componenti.append({"tipo": "checklist", "titolo": "Perche scegliere questo prodotto", "items": benefici})
        else:
            componenti.append(
                {
                    "tipo": "feature_grid",
                    "titolo": "Cosa ottieni",
                    "items": [{"titolo": item, "testo": ""} for item in benefici],
                }
            )

    if intro_titolo or intro_testo or image_url:
        componenti.append(
            {
                "tipo": "split_section",
                "titolo": intro_titolo or "Perche questa pagina conta",
                "testo": intro_testo or "Usa questa sezione per spiegare la proposta di valore con chiarezza.",
                "image_url": image_url,
                "image_alt": image_alt or titolo,
                "benefici": benefici if tipo in {"home", "landing"} else None,
            }
        )

    if cards:
        card_title = "Soluzioni in evidenza"
        if tipo == "category":
            card_title = "Sottocategorie o prodotti in evidenza"
        elif tipo == "product":
            card_title = "Dettagli chiave"
        componenti.append({"tipo": "feature_grid", "titolo": card_title, "items": cards})

    if testimonials and tipo in {"home", "landing", "product"}:
        componenti.append({"tipo": "testimonials", "titolo": "Cosa dicono i clienti", "items": testimonials})

    if prodotti_correlati and tipo == "product":
        componenti.append({"tipo": "product_cards", "titolo": "Spesso acquistato insieme", "items": prodotti_correlati})

    if faq:
        componenti.append({"tipo": "faq", "titolo": "Domande frequenti", "items": faq})

    componenti.append(
        {
            "tipo": "cta_band",
            "titolo": "Pronto a fare il passo successivo?",
            "testo": "Riduci dubbi e aumenta conversione con una CTA chiara e rassicurante.",
            "cta_primaria_testo": cta_primaria_testo or "Contattaci ora",
            "cta_primaria_url": cta_primaria_url or "/contatti/",
            "cta_secondaria_testo": cta_secondaria_testo,
            "cta_secondaria_url": cta_secondaria_url,
            "trust_items": trust_items or [],
        }
    )

    render_result = genera_blocchi_premium(componenti=componenti, titolo_pagina=titolo)
    render_result["tipo_pagina"] = tipo
    render_result["template"] = PAGE_TEMPLATES[tipo]
    return render_result


def revisiona_html_premium(contenuto_html: str, tipo_pagina: str | None = None) -> dict:
    html_source = contenuto_html or ""
    html_lower = html_source.lower()
    tipo = (tipo_pagina or "").strip().lower() or "landing"

    h1_count = len(re.findall(r"<h1\b", html_source, flags=re.IGNORECASE))
    h2_count = len(re.findall(r"<h2\b", html_source, flags=re.IGNORECASE))
    cta_count = len(re.findall(r"av-cta|aggiungi al carrello|ordina ora|verifica compatibilita|contattaci", html_lower))
    image_tags = re.findall(r"<img\b[^>]*>", html_source, flags=re.IGNORECASE)
    images_without_lazy = [tag for tag in image_tags[1:] if "loading=" not in tag.lower()]
    images_without_dimensions = [tag for tag in image_tags if "width=" not in tag.lower() or "height=" not in tag.lower()]
    long_paragraphs = []
    for raw in re.findall(r"<p\b[^>]*>(.*?)</p>", html_source, flags=re.IGNORECASE | re.DOTALL):
        if len(_strip_tags(raw).strip()) > 220:
            long_paragraphs.append(_strip_tags(raw).strip())

    min_h2 = {"home": 3, "landing": 3, "category": 2, "product": 3}.get(tipo, 3)
    rilevati = []
    patterns = {
        "hero": r"av-hero",
        "trust": r"av-trust-strip|spedizion|reso|sicur|compatibilita|garanzia|supporto",
        "stats": r"av-stats",
        "grid": r"av-grid",
        "testimonials": r"av-testimonial|recension",
        "faq": r"<dl|<dt|domande frequenti|faq",
        "price_box": r"av-price-box|\€|iva inclusa",
        "checklist": r"av-checklist",
        "split_section": r"av-split",
    }
    for nome, pattern in patterns.items():
        if re.search(pattern, html_lower):
            rilevati.append(nome)

    clarity = 100
    design = 100
    cro = 100
    performance = 100
    accessibility = 100

    blocker = []
    warning = []
    azioni = []

    if h1_count != 1:
        clarity -= 20
        accessibility -= 10
        blocker.append("La pagina deve avere esattamente un H1.")
        azioni.append("Correggi la gerarchia titoli: un solo H1, poi H2 e H3.")
    if h2_count < min_h2:
        clarity -= 15
        design -= 8
        warning.append(f"Pochi H2: trovati {h2_count}, consigliati almeno {min_h2}.")
        azioni.append("Aggiungi piu sezioni H2 per rendere la pagina scansionabile.")
    if cta_count < 1:
        cro -= 25
        blocker.append("Manca una CTA chiara.")
        azioni.append("Aggiungi almeno una CTA primaria esplicita.")
    elif cta_count == 1:
        cro -= 5
        warning.append("C'e una sola CTA: valuta una CTA finale di rinforzo piu in basso.")
    if tipo in {"home", "landing", "category", "product"} and "hero" not in rilevati:
        design -= 15
        cro -= 10
        warning.append("Manca una hero section riconoscibile sopra la piega.")
        azioni.append("Aggiungi una hero con promessa, sottotitolo e CTA.")
    if "faq" not in rilevati:
        cro -= 10
        warning.append("Manca una FAQ per abbattere obiezioni.")
        azioni.append("Aggiungi una FAQ con 3-5 domande reali dell'utente.")
    if "trust" not in rilevati:
        cro -= 12
        warning.append("Pochi trust signals visibili.")
        azioni.append("Aggiungi elementi di fiducia: spedizione, reso, supporto, compatibilita, sicurezza.")
    if not any(name in rilevati for name in ("stats", "testimonials", "price_box")):
        cro -= 10
        warning.append("Manca prova sociale o una prova quantitativa evidente.")
        azioni.append("Aggiungi statistiche, recensioni o un box prezzo/rating.")
    if len(rilevati) < 4:
        design -= 12
        warning.append("Pochi componenti visuali diversi: la pagina rischia di sembrare piatta.")
        azioni.append("Usa una combinazione di hero, card grid, split section, stats, trust strip e CTA band.")
    if long_paragraphs:
        clarity -= min(15, len(long_paragraphs) * 4)
        warning.append(f"Paragrafi troppo lunghi: {len(long_paragraphs)} rilevati.")
        azioni.append("Spezza i paragrafi lunghi in blocchi piu brevi e piu leggibili.")
    if images_without_lazy:
        performance -= min(15, len(images_without_lazy) * 4)
        warning.append("Ci sono immagini senza lazy loading dopo la prima immagine.")
        azioni.append("Aggiungi loading='lazy' a tutte le immagini non hero.")
    if images_without_dimensions:
        performance -= min(15, len(images_without_dimensions) * 4)
        accessibility -= 5
        warning.append("Ci sono immagini senza width/height espliciti.")
        azioni.append("Definisci width e height per evitare CLS.")
    if image_tags and tipo in {"home", "landing", "product"} and "fetchpriority=\"high\"" not in html_lower and "fetchpriority='high'" not in html_lower:
        performance -= 8
        warning.append("La prima immagine non sembra prioritizzata per LCP.")
        azioni.append("Per la hero usa fetchpriority='high' oppure preload dell'immagine principale.")
    if "clicca qui" in html_lower:
        cro -= 8
        clarity -= 5
        warning.append("Sono presenti CTA generiche tipo 'clicca qui'.")
        azioni.append("Rendi le CTA specifiche: 'Ordina ora', 'Verifica compatibilita', 'Contattaci'.")
    if re.search(r"color\s*:\s*#(?:111|000)|background\s*:\s*#(?:111|000)", html_lower):
        accessibility -= 5
        warning.append("Verifica eventuali colori inline scuri: rischiano di rompere il contrasto del tema.")

    clarity = max(0, clarity)
    design = max(0, design)
    cro = max(0, cro)
    performance = max(0, performance)
    accessibility = max(0, accessibility)
    totale = round((clarity + design + cro + performance + accessibility) / 5)

    return {
        "successo": True,
        "tipo_pagina": tipo,
        "punteggio_totale": totale,
        "punteggi": {
            "chiarezza": clarity,
            "design": design,
            "conversione": cro,
            "performance": performance,
            "accessibilita": accessibility,
        },
        "metriche": {
            "h1": h1_count,
            "h2": h2_count,
            "cta": cta_count,
            "immagini": len(image_tags),
            "paragrafi_lunghi": len(long_paragraphs),
        },
        "componenti_rilevati": rilevati,
        "blocker": blocker,
        "warning": warning,
        "azioni_prioritarie": azioni[:6],
        "pronto_per_pubblicare": totale >= 80 and not blocker,
        "workflow_consigliato": "Se il punteggio e sotto 80, migliora l'HTML e riesegui la review prima di pubblicare.",
    }