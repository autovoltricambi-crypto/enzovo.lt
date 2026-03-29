# SEO Tecnica

## Core Web Vitals (CWV)

Google usa i CWV come fattore di ranking. Misura la "salute" dell'esperienza utente.

### LCP — Largest Contentful Paint
Tempo di caricamento dell'elemento più grande visibile nella viewport.
- **Obiettivo:** < 2.5 secondi
- **Cause problemi:** immagini non ottimizzate, hosting lento, render-blocking CSS/JS
- **Soluzioni:** CDN, lazy loading, WebP, preload per immagini hero

### INP — Interaction to Next Paint (sostituisce FID da 2024)
Reattività della pagina alle interazioni utente.
- **Obiettivo:** < 200ms
- **Cause problemi:** JavaScript pesante, troppi plugin WordPress
- **Soluzioni:** ottimizza JS, rimuovi plugin inutili, usa cache

### CLS — Cumulative Layout Shift
Stabilità visiva: gli elementi si spostano durante il caricamento?
- **Obiettivo:** < 0.1
- **Cause problemi:** immagini senza dimensioni definite, font che si caricano tardi, ads
- **Soluzioni:** definisci width/height per immagini, usa font-display: swap

**Tool di misurazione:**
- Google PageSpeed Insights (test pagina specifica)
- Google Search Console → Core Web Vitals (dati reali)
- Chrome DevTools → Lighthouse

## Velocità del Sito

### Ottimizzazioni WordPress/WooCommerce

**Cache:**
- Plugin: WP Rocket (€49/anno, il migliore), LiteSpeed Cache (gratuito se hai LiteSpeed server), W3 Total Cache
- Abilita cache pagine, cache browser, minificazione CSS/JS

**Immagini:**
- Plugin: Smush, Imagify, ShortPixel
- Converti automaticamente in WebP
- Comprimi senza perdita di qualità visibile

**CDN (Content Delivery Network):**
- Cloudflare (gratuito) — distribuisce il sito su server globali
- Reduce TTFB (Time To First Byte)

**Hosting:**
- Shared hosting economico = lento per WooCommerce
- Consigliato: hosting WordPress gestito (Kinsta, WP Engine, Siteground)
- Minimo: PHP 8.2, MySQL 8, server europeo (per utenti italiani)

**Database:**
- WooCommerce accumula dati nel tempo → ottimizza regolarmente
- Plugin: WP-Optimize
- Cancella revisioni post, transient scaduti, log ordini vecchi

## Crawlability e Indicizzazione

### robots.txt
File che dice a Googlebot cosa scansionare e cosa no.

```
# Blocca aree admin e login
User-agent: *
Disallow: /wp-admin/
Disallow: /wp-login.php
Disallow: /cart/
Disallow: /checkout/
Disallow: /my-account/

# Permetti tutto il resto
Allow: /wp-admin/admin-ajax.php

# Sitemap
Sitemap: https://tuosito.it/sitemap_index.xml
```

### Sitemap XML
Lista di tutte le URL che vuoi indicizzare. WordPress + Yoast SEO la genera automaticamente.

**Tipi di sitemap:**
- `sitemap_index.xml` — indice principale
- `post-sitemap.xml` — articoli blog
- `page-sitemap.xml` — pagine statiche
- `product-sitemap.xml` — prodotti WooCommerce
- `product_cat-sitemap.xml` — categorie prodotti

**Invia la sitemap a Google:** Search Console → Sitemap → Aggiungi sitemap

### Redirect e Errori

**Redirect 301** (permanente — mantiene il valore SEO):
- Quando cambi URL di una pagina esistente
- Quando elimini una pagina e hai contenuto equivalente
- Da HTTP a HTTPS
- Da www a non-www (o viceversa)

**Errori 404** (pagina non trovata):
- Controlla regolarmente in Search Console → Copertura → Errori
- Se la pagina non esiste più → 301 alla categoria principale
- Se è un errore → correggi l'URL

**Catene di redirect:** evita A→B→C→D, usa sempre A→D direttamente

### Canonical Tag
Indica a Google quale è la versione "ufficiale" di una pagina quando ci sono URL duplicate.

```html
<link rel="canonical" href="https://tuosito.it/prodotto/filtro-olio-bmw/" />
```

**Quando usarlo:**
- Prodotti con varianti (diversi URL per colore/taglia)
- Pagine con parametri URL (filtri, sorting, pagination)
- Contenuto sindacato (pubblicato anche altrove)

Yoast SEO gestisce automaticamente i canonical per WooCommerce.

## HTTPS e Sicurezza

- HTTPS è un fattore di ranking confermato da Google
- Certificato SSL gratuito: Let's Encrypt (disponibile su quasi tutti gli hosting)
- Forza redirect HTTP → HTTPS in .htaccess o tramite plugin
- Mixed content: tutte le risorse (immagini, CSS, JS) devono essere HTTPS

## Mobile-First Indexing

Google indicizza la versione mobile del sito. Se la versione mobile è peggiore → ranking peggiore.

**Checklist mobile:**
- Tema responsive (WooCommerce Storefront o Astra sono ottimi)
- Bottoni e link facilmente cliccabili (min 44x44px)
- Testo leggibile senza zoom (min 16px)
- Nessun contenuto nascosto solo su mobile
- Stesso contenuto su desktop e mobile

## Struttura del Sito e Siloing

**Profondità click:** ogni pagina importante dovrebbe essere raggiungibile in max 3 click dalla homepage.

**Struttura ideale e-commerce:**
```
Homepage (1 click)
├── Categoria principale (1 click)
│   ├── Sottocategoria (2 click)
│   │   └── Prodotto (3 click)
```

**Breadcrumb:** aiutano Google e l'utente a capire la struttura
```
Home > Filtri > Filtri Olio > Filtro Olio BMW N47
```
WooCommerce + Yoast generano breadcrumb automaticamente con schema markup.

---

## Performance Web per WordPress + WooCommerce + Elementor

### Core Web Vitals

#### LCP - Largest Contentful Paint
- Obiettivo: `< 2.5s`.
- Tipicamente e l'immagine hero, il titolo principale o un banner above-the-fold.

**Come ottimizzarlo**
1. Cache pagina e TTFB basso.
2. Immagine hero in WebP/AVIF, dimensioni corrette, preload.
3. Meno CSS/JS render-blocking.

```html
<link rel="preload" as="image" href="/wp-content/uploads/hero-home.webp">
<img src="/wp-content/uploads/hero-home.webp" width="1280" height="720" fetchpriority="high" alt="Ricambi auto Auto Volt">
```

#### INP - Interaction to Next Paint
- Obiettivo: `< 200ms`.
- Peggiora con troppi script, widget Elementor, popup, chat e tracking ridondanti.

**Come ottimizzarlo**
1. Carica meno JS possibile.
2. Usa `defer` o delay per script non critici.
3. Evita librerie pesanti per interazioni semplici.

```html
<script defer src="/assets/app.js"></script>
```

#### CLS - Cumulative Layout Shift
- Obiettivo: `< 0.1`.

**Come evitarlo**
1. Dai `width` e `height` a immagini e iframe.
2. Riserva spazio per banner, recensioni, sticky bar.
3. Usa `font-display: swap`.

```html
<img src="/img/filtro.webp" width="400" height="400" alt="Filtro olio">
```

### Come misurare
- PageSpeed Insights: dati Google + laboratorio.
- Lighthouse: audit rapido in locale.
- GTmetrix: waterfall e debug richieste.
- Search Console: dati reali CWV.

### Immagini
1. Preferisci `AVIF`, poi `WebP`, poi JPG/PNG.
2. Non caricare immagini da 2000px se vengono mostrate a 400px.
3. `loading="lazy"` per tutto tranne la hero.

```html
<img
	src="/uploads/filtro-olio-400.webp"
	srcset="/uploads/filtro-olio-400.webp 400w, /uploads/filtro-olio-800.webp 800w"
	sizes="(max-width: 600px) 100vw, 400px"
	width="400"
	height="400"
	alt="Filtro olio Fiat Panda"
	loading="lazy"
	decoding="async"
>
```

**Plugin utili**
- ShortPixel
- Imagify
- EWWW Image Optimizer
- LiteSpeed Cache se il server e LiteSpeed

### CSS e JS
1. Genera Critical CSS o comunque carica subito solo l'above-the-fold.
2. Minifica e rimanda gli script non critici.
3. Rimuovi CSS inutilizzato e addon Elementor superflui.

```html
<style>
	body{margin:0;font-family:system-ui,sans-serif}
	.hero{min-height:60vh;display:grid;place-items:center}
</style>
<script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXX"></script>
<script defer src="/wp-content/themes/custom/app.js"></script>
```

### WordPress / WooCommerce specifico
- Cache: `LiteSpeed Cache` se disponibile, altrimenti `WP Rocket`.
- CDN: Cloudflare gratuito con Brotli e HTTP/3.
- Database: pulizia revisioni, transient, sessioni WooCommerce.
- Hosting: PHP 8.2+, NVMe, OPcache, HTTP/3.
- Se Elementor pesa troppo, le pagine piu importanti vanno rifatte in HTML/CSS diretto o Elementor molto pulito.

### Font Web
```css
@font-face {
	font-family: "Inter";
	src: url("/fonts/inter-regular.woff2") format("woff2");
	font-display: swap;
	font-weight: 400;
}
```

- Pochi pesi, pochi file, preferibilmente self-host.
- Preload solo del font sopra la piega.

### Checklist pratica per impatto
1. Cache pagina seria: `WP Rocket` o `LiteSpeed Cache`. Impatto `-0.8s / -2.5s`.
2. Hero image ottimizzata e preload. Impatto `-0.4s / -1.5s`.
3. Riduzione widget e addon Elementor. Impatto `-0.5s / -2s`.
4. Cloudflare con Brotli e HTTP/3. Impatto `-0.2s / -1s`.
5. Delay/defer JS non critico. Impatto `-0.3s / -1.2s`.
6. Font in `woff2` con `font-display: swap`. Impatto `-0.1s / -0.5s`.
7. CLS corretto su immagini e banner. Impatto forte su UX e punteggi.
8. Pulizia database WooCommerce. Impatto `-0.1s / -0.6s`.
9. Object cache / Redis se disponibile. Impatto `-0.2s / -0.8s`.
10. Cambio hosting se la base e debole. Impatto `-1s / -3s`.
