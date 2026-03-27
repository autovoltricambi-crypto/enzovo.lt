# Google Ads — Campagne Search

## Come Funziona la Search

Gli annunci Search appaiono quando l'utente cerca attivamente su Google. Paghi solo al click (CPC). È il formato con il più alto intento di acquisto.

**Struttura account:**
```
Account Google Ads
└── Campagna (budget, target geografico, rete)
    └── Gruppo Annunci (tema keyword)
        ├── Keyword
        └── Annunci (RSA)
```

## Tipi di Corrispondenza Keyword

| Tipo | Sintassi | Trigger |
|------|----------|---------|
| **Broad Match** | `filtro olio` | Qualsiasi query correlata (ampio) |
| **Phrase Match** | `"filtro olio"` | Query che contiene la frase |
| **Exact Match** | `[filtro olio bmw]` | Query esatta o varianti molto simili |

**Best practice per e-commerce:**
- Inizia con Phrase + Exact Match per controllare i costi
- Broad Match solo con Smart Bidding maturo (dopo 30+ conversioni/mese)
- Usa negative keyword per escludere traffico non rilevante

## Negative Keyword

Fondamentali per non sprecare budget:

```
Negative tipici per ricambi auto:
- "usato" (non vendi ricambi usati)
- "gratuito", "gratis", "free"
- "fai da te" (se non vuoi meccanici DIY)
- "schema", "manuale" (ricercano info, non prodotti)
- Modelli auto che non copri
```

**Liste negative:** crea liste condivise da applicare a tutte le campagne.

## Responsive Search Ads (RSA)

Formato standard dal 2022. Google combina automaticamente titoli e descrizioni.

**Struttura RSA:**
- 15 titoli (max 30 caratteri ciascuno)
- 4 descrizioni (max 90 caratteri ciascuna)
- Google testa le combinazioni migliori

**Linee guida per titoli:**
```
Titolo 1: [Keyword principale] — inserisci keyword dinamicamente
Titolo 2: [Beneficio principale] — "Spedizione Rapida in 24h"
Titolo 3: [USP] — "Ricambi OES Originali"
Titolo 4: [CTA] — "Acquista Online Ora"
Titolo 5: [Prezzo/offerta] — "Prezzi Competitivi"
Titolo 6: [Garanzia] — "Reso Gratuito 30 Giorni"
```

**Inserimento dinamico keyword (DKI):**
```
{KeyWord:Filtro Olio BMW}
```
→ Se la query è "filtro olio BMW serie 3", il titolo diventa "Filtro Olio BMW Serie 3"

## Estensioni Annunci (Asset)

Aumentano la visibilità senza costo aggiuntivo:

- **Sitelink:** link a pagine specifiche (categorie, offerte, contatti)
- **Callout:** frasi USP ("Reso Facile", "Assistenza Tecnica", "Pagamenti Sicuri")
- **Structured Snippet:** liste ("Marche: BMW, Fiat, Volkswagen, Opel")
- **Prezzo:** mostra prodotti con prezzi direttamente nell'annuncio
- **Immagine:** foto prodotto nell'annuncio (aumenta CTR)
- **Chiamata:** numero di telefono direttamente nell'annuncio

## Struttura Campagne per E-commerce Ricambi

### Struttura SKAG (Single Keyword Ad Group) — Tradizionale
Un gruppo annunci per keyword. Massimo controllo, alta manutenzione.

### Struttura Tematica — Raccomandata 2024
```
Campagna: Filtri Olio
├── Gruppo: Filtri Olio BMW
│   ├── [filtro olio bmw]
│   ├── [filtro olio bmw serie 3]
│   └── "filtro olio bmw n47"
├── Gruppo: Filtri Olio Fiat
│   └── [filtro olio fiat 500]
└── Gruppo: Filtri Olio Volkswagen
    └── [filtro olio vw golf]

Campagna: Pastiglie Freno
└── ...

Campagna: Brand + Competitors
└── [enzovo ricambi], [concorrente + ricambi]
```

## Quality Score

Il Quality Score (1-10) impatta il costo e la posizione dell'annuncio:

- **CTR atteso** (peso maggiore) — l'annuncio è rilevante per la query?
- **Rilevanza annuncio** — l'annuncio corrisponde alla keyword?
- **Esperienza landing page** — la pagina carica veloce? È pertinente?

**Migliorare QS:**
- Testo annuncio con la keyword esatta
- Landing page specifica (non homepage)
- Velocità pagina ottimizzata (CWV)

## Script Utili per E-commerce

**Pausa keyword con basso CTR (< 1%):**
```javascript
// In Google Ads Scripts
const keywords = AdsApp.keywords()
  .withCondition("Ctr < 0.01")
  .withCondition("Impressions > 500")
  .get();
while (keywords.hasNext()) {
  keywords.next().pause();
}
```

## Checklist Setup Campagna Search

- [ ] Conversioni configurate (acquisti WooCommerce)
- [ ] Keyword research completata
- [ ] Negative keyword aggiunte (almeno 20-30)
- [ ] RSA con 15 titoli e 4 descrizioni
- [ ] Tutte le estensioni configurate
- [ ] URL finali con UTM parameters
- [ ] Bid strategy impostata correttamente
- [ ] Target geografico: Italia (o regione specifica)
- [ ] Orario: escludi ore notturne se dati lo confermano
