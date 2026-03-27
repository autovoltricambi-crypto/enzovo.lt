# Meta Ads — Fondamenti

## Cos'è Meta Ads

Meta Ads (ex Facebook Ads) è la piattaforma pubblicitaria di Meta che include Facebook, Instagram, Messenger e Audience Network. A differenza di Google (intento attivo), Meta intercetta utenti in modo **interruttivo**: mostri l'annuncio a persone che non stavano cercando il tuo prodotto.

**Punti di forza:**
- Targeting demografico/interesse molto granulare
- Formato visivo (immagini, video, carousel)
- Costi più bassi rispetto a Google per awareness
- Retargeting potente

**Limiti:**
- Audience più fredda (non sta cercando attivamente)
- Richiede creatività accattivante per fermare lo scroll
- Post iOS 14.5 (2021): tracking meno preciso

## Struttura Account

```
Account Business (Business Manager)
└── Campagna (obiettivo, budget)
    └── Gruppo Inserzioni (audience, placement, budget)
        └── Inserzione (annuncio: testo + immagine/video)
```

## Obiettivi Campagna

### Awareness
- **Copertura:** massimizza persone raggiunte
- **Brand Awareness:** mostra a chi probabilmente ricorda l'annuncio

**Usa per:** sito nuovo, lancio prodotto, mercato nuovo.

### Consideration
- **Traffico:** click al sito
- **Engagement:** like, commenti, condivisioni
- **Visualizzazioni Video:** chi guarda il video

**Usa per:** generare traffico, crescere pagina.

### Conversion
- **Conversioni:** acquisti, lead, iscrizioni (richiede Pixel)
- **Vendite Catalogo:** mostra prodotti dal catalogo (retargeting dinamico)
- **Contatti:** lead form nativo su Facebook

**Per e-commerce:** usa sempre **Conversioni** ottimizzato per Acquisti.

## Meta Pixel

Il Pixel è un codice JavaScript che installi sul sito per tracciare le azioni degli utenti.

**Installazione WordPress:** plugin "Facebook for WooCommerce" (ufficiale Meta).

**Eventi standard per e-commerce:**
```javascript
// Visualizzazione prodotto
fbq('track', 'ViewContent', {
  content_ids: ['ELRING-163810'],
  content_type: 'product',
  value: 12.50,
  currency: 'EUR'
});

// Aggiunta al carrello
fbq('track', 'AddToCart', {
  content_ids: ['ELRING-163810'],
  value: 12.50,
  currency: 'EUR'
});

// Acquisto
fbq('track', 'Purchase', {
  value: 45.90,
  currency: 'EUR'
});
```

## Conversions API (CAPI)

Post iOS 14, molti eventi non vengono tracciati lato browser. La **Conversions API** invia gli eventi direttamente dal server di WooCommerce a Meta — più affidabile.

**Plugin:** Facebook for WooCommerce supporta CAPI nativamente.

**Deduplicazione:** usa lo stesso `event_id` sia nel Pixel che nella CAPI per evitare conteggi doppi.

## Struttura Budget

### Budget Campagna (CBO — Campaign Budget Optimization)
Meta distribuisce automaticamente il budget tra i gruppi inserzioni performanti.

**Vantaggi:** Meta ottimizza meglio di noi tra le audience.
**Svantaggi:** meno controllo su quale audience spende.

### Budget Gruppo Inserzioni (ABO — Ad Set Budget Optimization)
Budget fisso per ogni gruppo inserzioni.

**Usa quando:** vuoi testare audience specifiche con budget garantito.

## Funnel Meta Ads

```
TOP OF FUNNEL (ToFu) — Audience Fredda
↓ Interesse, Lookalike, Broad
↓ Obiettivo: Awareness o Traffic

MIDDLE OF FUNNEL (MoFu) — Audience Tiepida
↓ Visitatori sito, Engagement pagina
↓ Obiettivo: Conversioni (ATC, lead)

BOTTOM OF FUNNEL (BoFu) — Audience Calda
↓ Carrello abbandonato, Visitatori prodotto
↓ Obiettivo: Acquisto
```

## Metriche Chiave Meta Ads

| Metrica | Definizione | Target |
|---------|-------------|--------|
| **CPM** | Costo 1000 impressioni | €5-15 (varia molto) |
| **CTR** | Click/Impressioni | > 1% (immagine), > 2% (video) |
| **CPC** | Costo per click | < €0.50-1.50 |
| **CPP** | Costo per acquisto | Dipende dal margine |
| **ROAS** | Fatturato/Spesa | > 300% |
| **Frequency** | Volte visto/utente | < 3 (oltre → banner blindness) |

## Placement

**Automatico (consigliato):** Meta ottimizza su tutti i placement.

**Principali placement:**
- Facebook Feed
- Instagram Feed
- Instagram Stories/Reels
- Facebook Stories
- Audience Network (app esterne)
- Messenger

**Per e-commerce:** inizia con automatico, poi escludi i placement che non performano (Audience Network spesso bassa qualità).

## Checklist Fondamenti Meta Ads

- [ ] Business Manager configurato
- [ ] Pixel installato e verificato (Events Manager)
- [ ] Conversions API abilitata
- [ ] Evento Purchase tracciato con valore
- [ ] Catalogo prodotti collegato (per Dynamic Ads)
- [ ] Pagina Facebook e profilo Instagram collegati
- [ ] Metodo di pagamento configurato
