# Google Ads — Campagne Shopping

## Cos'è Google Shopping

Gli annunci Shopping mostrano immagine, titolo, prezzo e brand del prodotto direttamente nelle SERP. Richiedono un feed prodotti in Google Merchant Center.

**Vantaggi rispetto alla Search:**
- Visibilità visiva (immagine del prodotto)
- Prezzo visibile = traffico più qualificato
- Nessuna keyword da gestire (Google matcha automaticamente)
- CTR più alto per prodotti fisici

## Setup: Google Merchant Center

### 1. Creare l'Account GMC
- Vai su merchants.google.com
- Verifica proprietà sito (file HTML o DNS)
- Collega a Google Ads

### 2. Feed Prodotti

Il feed è il cuore di Shopping. Deve essere accurato e aggiornato.

**Attributi obbligatori:**
```
id          → SKU univoco (es. "ELRING-163810")
title       → Titolo prodotto (ottimizzato, max 150 char)
description → Descrizione (max 5000 char)
link        → URL pagina prodotto
image_link  → URL immagine principale
price       → Prezzo con valuta (es. "12.50 EUR")
availability → "in_stock" / "out_of_stock" / "preorder"
brand       → Marca del prodotto (es. "Elring")
gtin        → Codice EAN/UPC (se disponibile)
mpn         → Part number produttore (codice OE per ricambi)
condition   → "new"
google_product_category → Categoria Google (es. "Veicoli e Parti > Parti Auto")
```

**Attributi consigliati per ricambi:**
```
item_group_id    → Per varianti (es. stesso prodotto, taglie diverse)
custom_label_0   → Margine (es. "alto", "medio", "basso")
custom_label_1   → Categoria interna (es. "filtri-olio")
custom_label_2   → Stagionalità (es. "tutto-anno", "inverno")
custom_label_3   → Brand auto compatibile (es. "BMW")
```

### 3. Ottimizzazione Titoli Feed (Cruciale)

Il titolo è la keyword per Shopping. Google lo usa per matcharsi alle query.

**Formula ottimale per ricambi:**
```
[Marca ricambio] [Tipo prodotto] [Marca auto] [Modello] [Anno] [Codice motore]

Esempi:
"Elring Filtro Olio BMW Serie 3 2.0d N47 2007-2013"
"Bosch Pastiglie Freno Anteriori Fiat Punto 1.3 JTD 2003-2010"
"Bilstein Ammortizzatore Anteriore VW Golf V 1.6 FSI 2004-2009"
```

**Da evitare nel titolo:**
- Punteggiatura eccessiva
- Caratteri speciali non standard
- Termini promozionali ("OFFERTA", "SCONTO")

### 4. Aggiornamento Feed

- **Frequenza:** almeno 1 volta al giorno (prezzi e disponibilità cambiano)
- **Metodi:** URL feed (WooCommerce Product Feed plugin), API GMC, file FTP
- **Plugin WooCommerce consigliati:** WooCommerce Google Feed Manager, WPAE

## Struttura Campagne Shopping

### Standard Shopping
Controllo manuale su gruppi prodotto. Più controllo ma più lavoro.

```
Campagna Shopping — Filtri
├── Gruppo: Tutti i prodotti (bid basso, catch-all)
├── Gruppo: Filtri Olio (bid medio)
│   └── Suddivisi per: Marca ricambio → BMW → [prodotto specifico]
└── Gruppo: Filtri Aria (bid medio)
```

### Performance Max (PMax)
Dal 2022 ha sostituito Smart Shopping. Vedere `google-ads-performance-max.md`.

## Segmentare per Redditività

Usa i **custom_label** per separare prodotti per margine:

```
custom_label_0 = "alta-margine"  → bid aggressivo
custom_label_0 = "media-margine" → bid medio
custom_label_0 = "bassa-margine" → bid conservativo o escluso
```

## Ottimizzazione Shopping

### Search Terms Report
Analizza le query che hanno triggerato gli annunci:
- Aggiungi query rilevanti come negative keyword (se non vuoi quel traffico)
- Identifica prodotti che attirano traffico sbagliato

### Benchmark Metriche
| Metrica | Target E-commerce Ricambi |
|---------|--------------------------|
| CTR | 1-3% |
| CPC medio | €0.30-€1.50 |
| Conversion Rate | 1-4% |
| ROAS | 400-700% |

### Competitor Pricing
- Usa Google Merchant Center → Competitive visibility report
- Se il tuo prezzo è molto più alto → meno impression
- Monitora i competitor principali su strumenti come Price2Spy

## Errori Comuni Feed

| Errore | Causa | Soluzione |
|--------|-------|-----------|
| Prezzo non corrispondente | Prezzo feed ≠ prezzo sito | Aggiorna feed più frequentemente |
| Immagine non approvata | Immagine con testo/watermark | Usa immagini prodotto pulite |
| GTIN mancante per prodotti con barcode | Marche note richiedono GTIN | Inserisci EAN dal fornitore |
| Disponibilità non aggiornata | "in_stock" ma esaurito | Feed aggiornato almeno 1x/die |

## Checklist Shopping

- [ ] GMC verificato e collegato a Google Ads
- [ ] Feed con tutti gli attributi obbligatori
- [ ] Titoli ottimizzati con keyword
- [ ] Immagini prodotto di qualità (min 800x800px)
- [ ] Feed aggiornato automaticamente ogni giorno
- [ ] Custom labels configurate per margine
- [ ] Negative keyword campagna impostata
- [ ] Conversioni tracciate (acquisti)
