# Meta Ads — Retargeting e Dynamic Ads

## Retargeting su Meta

Il retargeting Meta mostra annunci a persone che hanno già interagito con il tuo brand: visitatori del sito, chi ha guardato i tuoi video, chi ha interagito con la tua pagina.

**Perché è il formato più efficiente:**
- Audience già consapevole del brand
- Più alta probabilità di conversione
- CPA tipicamente 2-5x inferiore all'acquisizione fredda

## Pixel e Tracking

Il Meta Pixel traccia le azioni degli utenti sul sito:

```javascript
// Visualizzazione prodotto (essenziale per retargeting dinamico)
fbq('track', 'ViewContent', {
  content_ids: ['ELRING-163810'],
  content_type: 'product',
  value: 12.50,
  currency: 'EUR',
  content_name: 'Filtro Olio BMW N47'
});

// Aggiunta al carrello
fbq('track', 'AddToCart', {
  content_ids: ['ELRING-163810'],
  content_type: 'product',
  value: 12.50,
  currency: 'EUR'
});

// Inizio checkout
fbq('track', 'InitiateCheckout', {
  value: 45.90,
  currency: 'EUR',
  num_items: 3
});

// Acquisto (conversione finale)
fbq('track', 'Purchase', {
  value: 45.90,
  currency: 'EUR',
  order_id: 'ORD-12345',
  content_ids: ['ELRING-163810', 'BOSCH-0986424504']
});
```

## Dynamic Product Ads (DPA)

Gli annunci dinamici mostrano automaticamente i prodotti che l'utente ha guardato sul sito — senza creare annunci manualmente per ogni prodotto.

### Setup

1. **Catalogo prodotti:** carica su Meta Business Manager → Catalogo → Crea (importa da feed WooCommerce)
2. **Pixel con eventi:** `ViewContent`, `AddToCart`, `Purchase` con `content_ids` corrispondenti agli ID nel catalogo
3. **Campagna:** Vendite → Vendite dal Catalogo → Retargeting

### Audience DPA

**Livelli di retargeting:**

```
Livello 1 (più caldo — entro 7 giorni):
→ "AddToCart ma non Purchase" ultimi 7 giorni
→ Budget: 40% del totale retargeting
→ Messaggio: "Completa il tuo ordine — ancora disponibile"
→ Eventuale piccolo sconto (5%)

Livello 2 (medio — entro 14 giorni):
→ "ViewContent ma non AddToCart" ultimi 14 giorni
→ Budget: 35%
→ Messaggio: "Stai ancora pensando a [prodotto]?"
→ Mostra recensioni del prodotto

Livello 3 (freddo — entro 30 giorni):
→ Tutti i visitatori sito ultimi 30 giorni
→ Budget: 25%
→ Messaggio: brand generale + offerta
```

### Creazione Annunci DPA

Il testo è statico, il prodotto è dinamico (viene dal catalogo):

```
Headline: "{{product.name}} — Compatibile con la tua auto"
Body: "Ricambi OES su enzovo.lt. Spedizione in 24h.
       Compatibilità garantita o rimborso. ✓"
CTA: "Acquista Ora"

→ Il prodotto, prezzo e immagine vengono automaticamente
  presi dal catalogo per ogni utente
```

## Sequenza Retargeting

### Metodo "Storia in 3 Atti"

**Act 1 — Reminder (Giorno 1-3):**
```
"Hai guardato [prodotto] su enzovo.lt"
→ Immagine prodotto + prezzo
→ CTA: "Torna al sito"
```

**Act 2 — Prova Sociale (Giorno 4-7):**
```
"1.247 clienti soddisfatti"
→ Carosello di recensioni
→ "Vedi le opinioni su Trustpilot"
→ CTA: "Compra con fiducia"
```

**Act 3 — Urgenza/Incentivo (Giorno 8-14):**
```
"Ultima chance — [prodotto] a prezzo speciale"
→ Sconto del 5-10% con codice
→ "Offerta valida solo per te, per 48 ore"
→ CTA: "Usa il codice BACK10"
```

**Dopo 14 giorni:** escludi dall'audience (non convertirà, stai sprecando budget).

## Retargeting per Segmento Prodotto

Con il catalogo Meta puoi targetizzare chi ha visitato specifiche categorie:

```
Audience: ViewContent → categoria "filtri" → ultimi 14gg
→ Annuncio: "Tutti i filtri BMW su enzovo.lt | da €9.90"
→ Mostra carousel di filtri BMW

Audience: ViewContent → categoria "freni" → ultimi 14gg
→ Annuncio: "Pastiglie e dischi freno | Spedizione domani"
→ Mostra carousel prodotti freni
```

## Cross-Sell via Retargeting

**Target:** chi ha già acquistato una volta.

```
Audience: Purchase ultimi 30-90 giorni
→ Escludi: Purchase ultimi 7 giorni (troppo presto)
→ Annuncio: prodotti complementari a quello acquistato

Logica:
SE acquisto == "filtro_olio" → mostra "filtro_aria" + "kit_guarnizioni"
SE acquisto == "pastiglie_anteriori" → mostra "dischi_anteriori" + "pastiglie_posteriori"
```

## Retargeting Video

Per chi ha guardato video su Facebook/Instagram:

```
Audience: Ha guardato >50% del video "Come cambiare filtro olio BMW"
→ Targeting: sanno cosa fare, hanno interesse pratico
→ Annuncio: "Hai gli strumenti — mancano solo i ricambi. [Prodotto] da €12.50"
```

## Esclusioni nel Retargeting

Sempre escludere:
- Clienti recenti (acquisto ultimi 7 giorni) → non annoiarli
- Persone che hanno visto l'annuncio 10+ volte senza cliccare → disinteressate

## Budget Allocation Retargeting

```
Budget mensile ads totale: €1.000

Acquisizione fredda: €600 (60%)
Retargeting: €400 (40%)
  - Carrello abbandonato 7gg: €160 (40%)
  - ViewContent 14gg: €140 (35%)
  - Visitatori 30gg: €100 (25%)
```

## Metriche Retargeting

| Metrica | Target |
|---------|--------|
| CTR | > 2% (alta perché audience calda) |
| Frequency | Max 7-10 in 7 giorni |
| CPP (Costo per Acquisto) | < 30% margine ordine medio |
| ROAS | > 500% |

## Checklist Retargeting Meta

- [ ] Pixel installato e verificato
- [ ] ViewContent, AddToCart, Purchase tracciati
- [ ] Catalogo prodotti creato e sincronizzato
- [ ] Custom Audience: ATC senza acquisto (7gg)
- [ ] Custom Audience: ViewContent senza ATC (14gg)
- [ ] Custom Audience: visitatori generici (30gg)
- [ ] Custom Audience: acquirenti recenti (per esclusioni)
- [ ] Campagna DPA configurata con 3 livelli
- [ ] Esclusioni configurate in ogni gruppo inserzioni
- [ ] Frequenza cap impostata (max 10/settimana)
- [ ] Conversions API per mitigare impatto iOS 14
