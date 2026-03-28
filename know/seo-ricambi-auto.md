# SEO per Ricambi Auto — Guida Operativa

## Logica di Ricerca degli Utenti

Chi cerca ricambi online usa tre tipi di query:

1. **Per codice OE** — "11427566327" (sa esattamente cosa cerca)
2. **Per compatibilità** — "filtro olio BMW Serie 3 2.0d" (conosce il veicolo)
3. **Per marca ricambio** — "filtro olio UFI BMW" (preferisce una marca)

Il sito deve comparire per TUTTE e tre le tipologie.

---

## Struttura URL

```
/prodotto/[tipo-ricambio]-[marca-ricambio]-[marca-auto]-[modello]-[motorizzazione]/
```

**Esempi corretti:**
```
/prodotto/filtro-olio-ufi-bmw-serie-3-2-0d-n47/
/prodotto/filtro-aria-mann-fiat-punto-1-4/
/prodotto/kit-distribuzione-dayco-fiat-1-3-multijet/
```

**Regole URL:**
- Solo minuscole, separatori con `-`
- No codici interni (no R304, no OP400)
- No caratteri speciali (niente puntini nei codici: `23-438-00` non `23.438.00`)
- Max 80 caratteri

---

## Struttura Categorie per SEO

```
Ricambi Auto
├── Filtri
│   ├── Filtri Olio
│   │   ├── Filtri Olio BMW
│   │   ├── Filtri Olio Fiat
│   │   ├── Filtri Olio Volkswagen
│   │   └── Filtri Olio Toyota
│   ├── Filtri Aria
│   └── Filtri Carburante
├── Distribuzione
│   ├── Kit Distribuzione
│   ├── Cinghie Distribuzione
│   └── Tenditore Distribuzione
├── Freni
│   ├── Pastiglie Freni
│   ├── Dischi Freno
│   └── Kit Freni
└── ...
```

**Ogni categoria deve avere:**
- H1 con keyword principale (es. "Filtri Olio per Auto")
- Testo introduttivo 150–300 parole
- Breadcrumb attivi
- Filtri per marca auto

---

## Title Tag per Prodotti

```
[Tipo Ricambio] [Marca Ricambio] [Auto] [Motore] | [Nome Sito]
```

**Esempi:**
```
Filtro Olio UFI BMW Serie 3 2.0d N47 | Enzovo
Filtro Aria Mann Fiat Punto 1.4 Natural Power | Enzovo
Kit Distribuzione Dayco Fiat 1.3 Multijet | Enzovo
```

**Regole:**
- Max 60 caratteri (senza nome sito)
- Keyword principale all'inizio
- Nome sito alla fine separato da `|`

---

## Meta Description per Prodotti

```
[Tipo ricambio] [marca] per [auto] [motore] ([anni]).
Codice OE: [codice]. Spedizione veloce, garanzia inclusa. Acquista online.
```

**Esempio:**
```
Filtro olio UFI per BMW Serie 3 318d/320d N47 (2005-2012).
Codice OE: 11427566327. Spedizione in 24h, garanzia 2 anni. Acquista online.
```

**Regole:**
- Max 155 caratteri
- Includere codice OE — molti utenti lo cercano direttamente
- Call to action finale

---

## Keyword Research per Ricambi Auto

### Keyword ad Alto Volume
- "[tipo ricambio] [marca auto]" → "filtro olio BMW", "filtro aria Fiat"
- "[tipo ricambio] [modello auto]" → "filtro olio Serie 3", "kit distribuzione Punto"
- "[tipo ricambio] [codice motore]" → "filtro olio N47", "filtro aria 1.3 Multijet"

### Keyword a Coda Lunga (alta conversione)
- "[tipo ricambio] [marca auto] [modello] [anno]" → "filtro olio BMW 320d 2008"
- "[tipo ricambio] [marca ricambio] [auto]" → "filtro olio UFI BMW Serie 3"
- "codice OE [codice]" → "codice OE 11427566327"
- "[SKU fornitore]" → "UFI 23.438.00", "Mann W712/83"

### Keyword Informazionali (blog/FAQ)
- "quando cambiare filtro olio [auto]"
- "quanto dura kit distribuzione [auto]"
- "filtro olio originale vs aftermarket"
- "intervallo cambio [ricambio] [auto]"

---

## Ottimizzazione Pagina Prodotto

### H1
```
[Marca Ricambio] — [Tipo Ricambio] per [Auto] [Motore]
```
Esempio: `UFI — Filtro Olio per BMW Serie 3 2.0d N47`

### H2 nella descrizione
- "Compatibilità veicoli"
- "Codici di riferimento"
- "Note di montaggio"

### Dati Strutturati (Schema.org)
Ogni prodotto deve avere markup:
```json
{
  "@type": "Product",
  "name": "Filtro Olio UFI BMW Serie 3 2.0d",
  "sku": "UFI-23.438.00",
  "brand": {"@type": "Brand", "name": "UFI"},
  "offers": {
    "@type": "Offer",
    "price": "12.50",
    "availability": "InStock"
  }
}
```

---

## SEO per Codici OE e SKU

I codici OE (es. `11427566327`) e SKU fornitore (es. `UFI-23.438.00`) sono keyword ad alta conversione — chi cerca un codice esatto è pronto all'acquisto.

**Dove inserire i codici:**
- Nella descrizione prodotto (sezione "Codici di riferimento")
- In un campo attributo WooCommerce visibile
- Nel meta description
- Nel testo alternativo immagine (se pertinente)

**Formato per la leggibilità:**
- Codice OE BMW: `11427566327`
- Codice UFI: `23.438.00`
- Non modificare il formato originale — gli utenti cercano esattamente quello

---

## Link Interni

### Da categoria a prodotto
Ogni pagina categoria deve linkare ai prodotti più venduti.

### Cross-selling tra marche
I prodotti con stesso `related_sku_code` sono equivalenti → linkali tra loro:
```
"Vedi anche: Filtro Olio Mann W712/83 (equivalente)"
"Vedi anche: Filtro Olio Mahle OC1044 (equivalente)"
```

### Link per marca auto
Ogni prodotto deve linkare alla categoria "Filtri Olio BMW" corrispondente.

---

## Contenuti Blog per SEO

### Argomenti ad alto traffico per ricambi auto:
- "Quando cambiare il filtro olio [marca auto] [modello]"
- "Filtro olio originale vs aftermarket: differenze e costi"
- "Kit distribuzione [auto]: quando sostituirlo e quanto costa"
- "Guida ai codici OE: cosa sono e come usarli"
- "Migliori marche di filtri auto: UFI, Mann, Mahle a confronto"

### Struttura articolo SEO:
1. H1 con keyword principale
2. Introduzione con keyword (primo paragrafo)
3. H2 per ogni sottosezione
4. Link interni ai prodotti pertinenti
5. FAQ con markup schema.org

---

## Velocità e Core Web Vitals

Per un sito di ricambi con molti prodotti:
- Immagini WebP, max 200KB per prodotto
- Lazy loading immagini sotto the fold
- Cache aggressiva per pagine prodotto statiche
- Evitare plugin pesanti che rallentano il caricamento

---

## Checklist SEO per Ogni Nuovo Prodotto

- [ ] Titolo con marca ricambio + tipo + auto + motore
- [ ] URL con slug ottimizzato (no codici interni)
- [ ] Meta description con codice OE e call to action
- [ ] Descrizione con compatibilità veicoli dettagliata
- [ ] Codice OE inserito nel testo
- [ ] Categoria corretta assegnata
- [ ] Attributi WooCommerce compilati (marca auto, modello, anno, codice OE)
- [ ] Immagine con alt text descrittivo
- [ ] Link interno alla categoria principale
