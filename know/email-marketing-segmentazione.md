# Email Marketing — Segmentazione

## Cos'è la Segmentazione

La segmentazione divide la lista email in gruppi omogenei per inviare messaggi più rilevanti. Email rilevanti = open rate più alto, conversioni migliori, meno disiscrizioni.

**Regola d'oro:** l'email giusta, alla persona giusta, al momento giusto.

## Tipi di Segmentazione

### 1. Demografica
- Città/regione
- Età (se raccolta)
- Lingua

### 2. Comportamentale (la più potente per e-commerce)
- Acquirenti vs non acquirenti
- Acquirenti frequenti vs occasionali
- Spesa media
- Categoria prodotti acquistati
- Data ultimo acquisto
- Prodotti visualizzati

### 3. RFM — Il Framework Fondamentale

**RFM = Recency, Frequency, Monetary Value**

| Dimensione | Cosa misura |
|------------|-------------|
| **Recency** | Quando ha acquistato l'ultima volta |
| **Frequency** | Quante volte ha acquistato |
| **Monetary** | Quanto ha speso in totale |

**Segmenti RFM:**

```
CHAMPIONS (alto R, alto F, alto M)
→ Acquistano spesso, di recente, spendono tanto
→ Strategia: ricompensa, chiedi recensioni, fai ambasciatori

LOYAL CUSTOMERS (medio-alto F, medio M)
→ Acquistano regolarmente
→ Strategia: programma fedeltà, upsell

AT RISK (basso R, un tempo alto F)
→ Erano buoni clienti, non comprano più
→ Strategia: win-back aggressivo, offerta forte

LOST (basso R, bassa F, bassa M)
→ Hanno comprato una volta tanto fa
→ Strategia: win-back economico o soppressione

NEW CUSTOMERS (alto R, bassa F)
→ Primo acquisto recente
→ Strategia: fidelizza, secondo acquisto

POTENTIAL LOYALISTS (medio R, media F)
→ Comprano ma non ancora regolari
→ Strategia: spingi alla fedeltà con programma
```

### 4. Engagement Email
- **Attivi:** aperti email negli ultimi 90 giorni
- **Semi-attivi:** aperti nell'ultimo anno
- **Inattivi:** non aprono da 12+ mesi

**Strategia per inattivi:**
1. Campagna re-engagement ("Ci sei ancora?")
2. Se non reagiscono dopo 3 email → rimuovi dalla lista attiva
3. Mantieni in lista separata (non cancellare — usano dati storici)

### 5. Ciclo di Vita del Cliente

```
Prospect → Nuovo Cliente → Cliente Attivo → Cliente Fedele → Inattivo → Perso
```

Ogni fase richiede una comunicazione diversa:
- **Prospect:** converti al primo acquisto
- **Nuovo:** fidelizza al secondo acquisto
- **Fedele:** upsell, cross-sell, referral
- **Inattivo:** win-back

## Segmentazione Specifica per Ricambi Auto

### Per Marca Auto
```
Segmento BMW → email su ricambi BMW, guide BMW, offerte BMW
Segmento Fiat → email su ricambi Fiat
Segmento VW Group → ricambi VW, Audi, Skoda, Seat
```

**Come raccogliere la marca auto:**
- Campo nel form di iscrizione: "Qual è la tua auto?"
- Campo al checkout: "Modello del veicolo"
- Quiz lead magnet: "Trova i ricambi per la tua auto"

### Per Tipo di Ricambio Acquistato
```
Segmento "Filtri" → email filtri, bundle manutenzione
Segmento "Freni" → email pastiglie, dischi, kit freno
Segmento "Elettrico" → candele, sensori, batterie
```

### Per Frequenza Manutenzione
- Se compra filtri ogni 15.000km → email preventiva prima della scadenza
- "Sono passati 6 mesi dal tuo ultimo filtro olio — è ora di cambiarlo?"

## Implementazione in Klaviyo

### Segmento Attivi
```
Condizioni:
- Ha aperto email negli ultimi 90 giorni
- E ha fatto almeno 1 ordine
```

### Segmento Champions
```
Condizioni:
- Numero ordini ≥ 3
- E valore totale ordini ≥ €150
- E data ultimo ordine negli ultimi 60 giorni
```

### Segmento At Risk
```
Condizioni:
- Numero ordini ≥ 2
- E data ultimo ordine tra 91 e 180 giorni fa
```

### Segmento BMW
```
Condizioni:
- Ha proprietà "marca_auto" = "BMW"
- OPPURE ha acquistato prodotto con tag "BMW"
```

## Lista Pulita — Igiene della Lista

**Rimuovi regolarmente:**
- Hard bounce (email non esistente) → rimuovi subito
- Soft bounce ripetuti (5+ volte) → rimuovi
- Inattivi da 12+ mesi (dopo tentativo re-engagement)
- Spam complaint → rimuovi immediatamente

**Frequenza pulizia:** ogni 3-6 mesi.

**Perché:** una lista pulita ha open rate più alta → migliore deliverability → meno spam.

**Strumento:** Klaviyo lista "Never opened" → supprimere dopo campagna re-engagement.

## Personalizzazione Dinamica

Usa variabili nel testo per personalizzare automaticamente:

```
Ciao {{ first_name | default: "automobilista" }},

I tuoi ricambi per la {{ customer.marca_auto | default: "tua auto" }}
sono arrivati nuovi in catalogo.

Il tuo ultimo ordine era {{ last_order_date }}.
```

## Checklist Segmentazione

- [ ] Segmenti RFM configurati (almeno Champions, At Risk, New)
- [ ] Segmento attivi/inattivi
- [ ] Segmento per marca auto (se dati disponibili)
- [ ] Segmento per categoria acquistata
- [ ] Segmenti di ciclo vita configurati
- [ ] Pulizia lista programmata ogni 3 mesi
- [ ] Personalizzazione nome in tutte le email
- [ ] Test di deliverability prima di grandi invii (>10k email)
