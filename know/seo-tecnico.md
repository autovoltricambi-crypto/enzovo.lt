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
