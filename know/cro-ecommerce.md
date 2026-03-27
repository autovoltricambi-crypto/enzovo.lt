# CRO — Ottimizzazione E-commerce

## Il Funnel E-commerce e i Punti di Perdita

```
100 visitatori
    ↓ 40% visualizzano una categoria
40 visitatori categoria
    ↓ 50% visitano una pagina prodotto
20 visitatori pagina prodotto
    ↓ 30% aggiungono al carrello
6 aggiungono al carrello
    ↓ 50% iniziano il checkout
3 iniziano checkout
    ↓ 67% completano
2 acquisti

Conversion Rate: 2%
```

Ogni step è un'opportunità di ottimizzazione.

## Pagina Prodotto — Ottimizzazione Completa

### Sopra the Fold (Senza Scorrere)
Deve rispondere immediatamente a: "È il prodotto giusto? Costa quanto mi aspetto? Posso fidarmi?"

**Elementi obbligatori:**
```
[Titolo prodotto con keyword e specifiche]
[Immagini prodotto di qualità — min 4-5 angolazioni]
[Prezzo ben visibile]
[Pulsante "Aggiungi al Carrello" prominente]
[Disponibilità: "In Stock — Spedito domani"]
[Compatibilità veicolo verificata]
[Badge fiducia: SSL, reso, spedizione]
```

### Sotto the Fold
```
[Descrizione dettagliata]
[Specifiche tecniche in tabella]
[Lista compatibilità veicoli]
[Istruzioni installazione (video o testo)]
[Recensioni clienti]
[Prodotti correlati / "Acquistati insieme"]
[FAQ sulla compatibilità]
```

### Bottone CTA
- Colore contrastante (non grigio)
- Testo specifico: "Aggiungi al Carrello" o "Acquista Ora"
- Dimensioni grandi, visibile senza scorrere
- Su mobile: fisso in basso (sticky)

### Tabella Compatibilità
Per ricambi auto, la compatibilità è la domanda principale:
```
| Marca | Modello | Anno | Motore | Codice OE |
|-------|---------|------|--------|-----------|
| BMW | Serie 3 (E90) | 2005-2012 | 2.0d N47 | 11427566327 |
| BMW | Serie 5 (E60) | 2004-2010 | 2.0d N47 | 11427566327 |
```

Tool di verifica compatibilità → riduce drasticamente i resi.

### Immagini
- Min 5 immagini: fronte, retro, lato, dettaglio, in contesto
- Zoom on hover
- Immagine con dimensioni fisiche (righello o mano come riferimento)
- Video installazione (aumenta conversioni del 30-40%)

## Pagina Checkout — Il Momento Critico

Il checkout è dove si perde il 70-75% degli acquirenti. Ogni punto di attrito = soldi persi.

### Ottimizzazioni Obbligatorie

**Guest checkout:**
- Non obbligare la registrazione
- "Continua come ospite" sempre disponibile
- Offri di creare account DOPO l'acquisto

**Numero di passi:**
- Ideale: 1-2 pagine (non 4-5)
- Mostra progress bar ("Passo 2 di 3")
- Non chiedere informazioni non necessarie

**Campi form:**
- Solo l'essenziale (nome, email, indirizzo, pagamento)
- Validazione in tempo reale (non solo dopo submit)
- Autocomplete indirizzo (Google Places API)
- Campo "Note ordine" non obbligatorio

**Pagamenti:**
- Accetta: carta (Stripe), PayPal, bonifico
- Apple Pay / Google Pay per mobile (conversione +30%)
- "Paga in 3 rate" (Scalapay, Klarna) per ordini > €50

**Rassicurazioni nel checkout:**
```
🔒 Pagamento sicuro SSL
📦 Spedizione gratuita sopra €35
↩️ Reso gratuito 30 giorni
```

**Riepilogo ordine visibile** con immagini prodotti, quantità, prezzi.

### Checkout per Mobile
- Touch target min 44x44px
- Tastiera numerica per campi numero/carta
- Testo min 16px
- Senza elementi ingombranti
- Test reale su iPhone e Android

## Carrello — Ridurre l'Abbandono

**Aggiunte al carrello che non abbandonano:**

```
✓ Free shipping threshold: "Aggiungi €12 per la spedizione gratuita"
✓ Trust badge nel carrello
✓ Immagini prodotto nel carrello
✓ Bottone checkout ben visibile
✓ Opzione "Salva per dopo"
✓ Estimated delivery date
```

**Cross-sell nel carrello:**
```
"Spesso acquistati insieme:
□ Filtro olio BMW N47 (già nel carrello)
□ Filtro aria BMW N47 (+€11.90) [Aggiungi]
□ Kit guarnizioni scarico N47 (+€8.50) [Aggiungi]"
```

## Social Proof — Dove Inserirla

| Posizione | Tipo di Proof |
|-----------|--------------|
| Homepage | Numero clienti, recensioni aggregate |
| Pagina categoria | "Più venduto", badge "Bestseller" |
| Pagina prodotto | Recensioni con stelle, Q&A |
| Vicino al CTA | "1.247 acquistati questo mese" |
| Checkout | "Pagamento sicuro come X altri clienti" |
| Email | "Marco da Milano ha appena ordinato" |

## Upsell e Cross-sell

### Order Bumps (al checkout)
Offerta semplice da aggiungere con 1 click prima del pagamento:
```
"Aggiungi anche: Kit guarnizioni scarico — solo €6.90 invece di €9.90"
[✓ Sì, aggiungi al mio ordine]
```

### Post-Purchase Upsell
Dopo il pagamento, offerta a prezzo scontato:
```
"Grazie per il tuo ordine!
Prima di confermare la spedizione, vuoi aggiungere:
Filtro aria compatibile — €11.90 (spedizione già pagata)
[Sì, aggiungilo] [No grazie]"
```

### Prodotti Correlati (Cross-sell)
Su pagina prodotto e nel carrello:
```
"Acquistati spesso insieme:
Filtro olio + Filtro aria + Kit guarnizioni
Insieme: €27.90 (risparmi €4.90)"
```

## Speed — Impatto sulla Conversione

Ogni secondo di ritardo = -7% conversioni.

**Target:**
- LCP < 2.5 secondi
- TTI < 3.5 secondi su mobile

**Strumenti di test:**
- PageSpeed Insights → punteggio e suggerimenti
- GTmetrix → analisi dettagliata
- WebPageTest → test da diverse location

**Quick wins WooCommerce:**
- CDN (Cloudflare free)
- Plugin cache (WP Rocket)
- Immagini WebP + lazy load
- Rimuovi plugin inutili

## Checklist CRO E-commerce

### Pagina Prodotto
- [ ] CTA sopra the fold su tutti i dispositivi
- [ ] Min 4 immagini prodotto di qualità
- [ ] Tabella compatibilità veicoli
- [ ] Prezzo + disponibilità ben visibili
- [ ] Trust badge vicino al CTA
- [ ] Recensioni con foto (se possibile)

### Checkout
- [ ] Guest checkout abilitato
- [ ] Max 2 pagine checkout
- [ ] Progress bar visibile
- [ ] Apple Pay / Google Pay
- [ ] Rassicurazioni (SSL, reso, spedizione) visibili
- [ ] Test su mobile reale

### Carrello
- [ ] Free shipping threshold indicator
- [ ] Cross-sell nel carrello
- [ ] Immagini prodotti nel carrello
- [ ] Bottone checkout prominente

### Performance
- [ ] PageSpeed > 70 su mobile
- [ ] LCP < 2.5s su 3G
