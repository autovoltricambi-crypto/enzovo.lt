# SEO — On-Page Optimization

## Elementi On-Page da Ottimizzare

### Title Tag
Il titolo che appare nei risultati Google (il più importante elemento on-page).

**Regole:**
- Max 60 caratteri (altrimenti viene troncato)
- Keyword principale all'inizio
- Brand alla fine (opzionale)
- Ogni pagina deve avere un title unico

**Formula per e-commerce:**
```
[Keyword Principale] | [Brand] — oppure —
[Prodotto] [Modello] [Anno] — Acquista Online | NomeSito
```

**Esempi:**
- ✓ "Filtro Olio BMW Serie 3 N47 — Elring 163.810 | enzovo.lt"
- ✗ "Prodotto #1234 - Categoria - Sito"

### Meta Description
Non è un fattore di ranking diretto ma influenza il CTR (click-through rate).

**Regole:**
- Max 155-160 caratteri
- Include keyword principale (Google la mette in grassetto)
- Call-to-action chiara: "Acquista ora", "Scopri", "Risparmia"
- Unica per ogni pagina

**Formula:**
```
[Beneficio principale]. [Dettaglio tecnico]. [CTA con urgenza/valore].
```

**Esempio:**
"Filtro olio Elring per BMW Serie 3 2.0d N47. Codice OE 11427566327. Spedizione rapida ✓ Reso facile ✓ Prezzi competitivi."

### Heading Tags (H1, H2, H3)

**H1:**
- Un solo H1 per pagina
- Contiene la keyword principale
- Leggermente diverso dal title tag (non copiare-incollare)

**H2 e H3:**
- Strutturano il contenuto (sommario logico)
- Includono keyword secondarie e LSI (Latent Semantic Indexing)
- Aiutano Google a capire l'argomento della pagina

**Esempio struttura pagina prodotto:**
```
H1: Filtro Olio BMW Serie 3 2.0d — Elring 163.810
  H2: Specifiche Tecniche
  H2: Compatibilità Veicoli
  H2: Come Montarlo
  H2: Prodotti Correlati
```

### URL Structure

**Buone pratiche:**
- Brevi e descrittivi
- Keyword principale nell'URL
- Parole separate da trattini (non underscore)
- Solo minuscolo
- Nessun carattere speciale

**Formula e-commerce:**
```
/[categoria]/[sottocategoria]/[prodotto-keyword/
/filtri-olio/bmw/filtro-olio-bmw-serie-3-n47-elring/
```

### Contenuto della Pagina

**Lunghezza:**
- Pagine categoria: 300-500 parole di testo descrittivo + prodotti
- Pagine prodotto: 200-400 parole di descrizione dettagliata
- Articoli blog: 1.500-3.000 parole per keyword competitive

**Densità keyword:**
- Non esiste un % magico — scrivi per l'utente, non per Google
- Usa varianti e sinonimi (LSI keywords)
- Evita il keyword stuffing (penalizzazione)

**Testo descrittivo unico:**
- MAI copiare descrizioni dal fornitore (duplicate content)
- Aggiungi: compatibilità veicolo, note di montaggio, vantaggi del prodotto
- Include codici OE e cross-reference

### Ottimizzazione Immagini

**Nome file:** `filtro-olio-bmw-n47-elring-163810.jpg` (non `IMG_1234.jpg`)

**Alt text:** descrizione dell'immagine con keyword
- ✓ `alt="Filtro olio Elring 163.810 per BMW Serie 3 N47 2.0d"`
- ✗ `alt="filtro"` o `alt=""`

**Formato e dimensioni:**
- WebP (migliore compressione) o JPEG per foto
- Max 100-200KB per immagine prodotto
- Dimensione: 800x800px per prodotti (WooCommerce la ridimensiona)

**Lazy loading:** le immagini sotto the fold devono usare lazy loading (WordPress lo fa di default)

### Link Interni

Collegano le pagine del sito tra loro:
- Aiutano Google a scoprire e indicizzare le pagine
- Distribuiscono l'"autorità" (link equity)
- Migliorano l'esperienza utente

**Strategie per e-commerce:**
- Dalla homepage alle categorie principali
- Dalle categorie ai prodotti
- Dai prodotti a prodotti correlati e complementari
- Dal blog ai prodotti correlati

**Anchor text:** usa keyword descrittive, non "clicca qui"
- ✓ "filtri olio per BMW"
- ✗ "clicca qui" o "scopri di più"

### Schema Markup (Dati Strutturati)

WooCommerce genera automaticamente Product schema. Verifica e aggiungi:

```json
{
  "@type": "Product",
  "name": "Filtro Olio BMW Serie 3 N47",
  "sku": "ELRING-163810",
  "brand": {"@type": "Brand", "name": "Elring"},
  "offers": {
    "@type": "Offer",
    "price": "12.50",
    "priceCurrency": "EUR",
    "availability": "InStock"
  }
}
```

Plugin consigliato: **Yoast SEO** (gestisce automaticamente molti schema).
