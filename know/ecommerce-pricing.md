# E-commerce — Pricing Strategy

## Principi del Pricing

Il prezzo non è solo un numero — è un segnale di valore, posizionamento e competitività. La strategia di pricing sbagliata può costare più delle campagne ads ottimizzate male.

**Obiettivi pricing:**
1. Coprire i costi e generare margine
2. Essere competitivo rispetto ai concorrenti
3. Comunicare il valore del prodotto
4. Massimizzare il fatturato (non sempre il prezzo più basso)

## Calcolo Prezzo Minimo

### Formula Base

```
Prezzo Minimo = Costo prodotto / (1 - Margine desiderato)

Esempio:
Costo prodotto: €8.00
Margine desiderato: 35%
→ Prezzo minimo = €8.00 / (1 - 0.35) = €12.31 (netto IVA)
→ Prezzo finale con IVA 22%: €12.31 × 1.22 = €15.02
```

### Tutti i Costi da Considerare

```
Costo prodotto:           €8.00
Spedizione (se gratuita): €4.50 (media Italia)
Imballo:                  €0.30
Commissioni pagamento:    €0.43 (Stripe 1.4% + €0.25 su €15)
Resi/difetti (2%):        €0.30
Quota ads per ordine:     €2.00 (se CPA ads €2)
Overhead (hosting,ecc):   €0.50
─────────────────────────────
Costo totale:             €16.03

Prezzo vendita:           €15.02 (netto IVA)
Margine lordo:            -€1.01 (PERDITA!)

→ Il prezzo deve essere almeno €16.03 / (1-0) = €19.55 per coprire tutto
→ Con margine 20% netto: €16.03 / 0.80 = €20.04
```

## Strategie di Pricing

### 1. Cost-Plus (Costo + Margine)

Aggiungi un margine fisso al costo.

```
Costo: €8 → Margine 40% → Prezzo €13.33 (netto)
```

**Pro:** semplice, garantisce margine.
**Contro:** ignora la concorrenza e la percezione del valore.

### 2. Competitive Pricing (Basato sulla Concorrenza)

Monitora i prezzi dei competitor e posizionati strategicamente.

```
Competitor A: €14.90
Competitor B: €13.50
Competitor C: €15.20

Strategia parity: €14.50 (leggermente sotto la media)
Strategia premium: €15.90 (sopra, se hai valore superiore)
Strategia low cost: €12.90 (sotto tutti, se vuoi volume)
```

**Come monitorare:**
- Price2Spy: monitoraggio automatico prezzi competitor
- Manuale: controlla AutoDoc, eBay, Amazon periodicamente

### 3. Value-Based Pricing

Prezza in base al valore percepito, non al costo.

```
Filtro olio OES Elring (valore alto):
→ Il cliente sa che è lo stesso del concessionario
→ Prezzo: €15-18 (premium sostenibile)

Filtro olio aftermarket generico:
→ Valore percepito inferiore
→ Prezzo: €8-10 (competitivo)
```

### 4. Dynamic Pricing

Aggiusta il prezzo in base a domanda, stagione, stock, competitor.

**Trigger per alzare prezzo:**
- Stock basso (< 5 pezzi)
- Competitor esauriti
- Alta domanda stagionale

**Trigger per abbassare prezzo:**
- Stock alto (> 50 pezzi)
- Concorrenza molto aggressiva su quel prodotto
- Prodotto vicino a fine vita

**Tool:** Wiser, RepricerExpress, o manuale con monitoraggio.

### 5. Bundle Pricing

Vendi più prodotti insieme a prezzo vantaggioso.

```
Kit Tagliando BMW N47:
- Filtro olio Elring: €12.50
- Filtro aria Mann: €14.90
- Kit guarnizioni scarico: €8.50
Totale singoli: €35.90
Bundle: €29.90 (-17%)

→ AOV aumenta del 150%
→ Margine assoluto quasi uguale (risparmi su spedizione e acquisizione)
```

**Tipi di bundle:**
- **Kit stagionali:** "Kit inverno BMW" (filtri + batteria + liquido antigelo)
- **Kit intervento:** tutto per un intervento specifico
- **Kit modello:** top 5 ricambi per BMW E90 in kit

### 6. Anchor Pricing

Mostra un prezzo di riferimento più alto per far sembrare il tuo prezzo un affare.

```
~~Prezzo concessionario: €45.00~~
Il nostro prezzo: €12.50
Risparmio: €32.50 (72%)
```

**Attenzione:** il prezzo "barrato" deve essere reale (non inventato) per rispettare le norme UE (Direttiva Omnibus 2022).

**Direttiva Omnibus:** il prezzo "prima" deve essere il più basso degli ultimi 30 giorni.

## Psicologia dei Prezzi

### Prezzi "Charm" (Terminanti in .9 o .99)
```
€14.99 sembra significativamente meno di €15.00
€12.90 sembra "intorno ai 12", non ai 13
```
**Quando usare:** prodotti commodity, fascia bassa.
**Quando evitare:** prodotti premium (usa cifre tonde: €15, €20).

### Price Bracketing (Decoy Effect)

```
Opzione A: Filtro base — €8.90
Opzione B: Filtro OES — €12.90 ← vuoi vendere questo
Opzione C: Kit completo — €29.90

→ Il cliente confronta A e B: "solo €4 in più per OES? Prendo OES"
→ L'Opzione B vende di più grazie all'ancoraggio
```

### Soglie Spedizione Gratuita

```
Spedizione gratuita sopra €35

Se ordine medio è €28 → cliente aggiunge un prodotto da €7 per arrivare a €35
→ AOV sale, costo spedizione viene assorbito
```

**Ottimizzazione:** soglia = AOV medio + 20-30%.

## Pricing per Categoria

| Categoria | Margine Target | Strategia |
|-----------|---------------|-----------|
| Filtri olio | 35-45% | Competitivo (molta concorrenza) |
| Kit tagliando | 30-40% | Bundle, valore percepito alto |
| Pastiglie freno | 40-50% | Qualità/sicurezza = premium ok |
| Ammortizzatori | 35-45% | Competitivo su marche note |
| Ricambi rari | 50-60% | Meno concorrenza, meno pressione |
| Accessori | 50-70% | Alta marginalità, bassa pressione |

## Gestione Prezzi in WooCommerce

### Plugin per Dynamic Pricing
- **WooCommerce Dynamic Pricing:** sconti per quantità, ruolo utente
- **Discount Rules for WooCommerce:** regole avanzate

### Prezzi per Livello Cliente
```
Ospite/Base: prezzo standard
Clienti registrati: -5%
Clienti VIP (>€500 spesi): -10%
```

### Arrotondamento Automatico
Imposta prezzi finali a XX.90 o XX.00 automaticamente:

```php
// functions.php
add_filter('woocommerce_product_get_price', function($price, $product) {
  return ceil($price * 10) / 10 - 0.10; // arrotonda a .90
}, 10, 2);
```

## Monitoraggio Margini

### Report Mensile Margini

```
Prodotto | Vendite | Fatturato | Costo | Margine % | Margine €
Elring 163810 | 45 | €562.50 | €360 | 36% | €202.50
Mann W712 | 38 | €456 | €304 | 33% | €152
...
```

Identifica prodotti con margine < 20% → rivedi prezzo o fornitore.

## Checklist Pricing

- [ ] Costo totale per prodotto calcolato (inclusi tutti i costi)
- [ ] Margine minimo definito (es. 30% netto)
- [ ] Monitoring prezzi competitor configurato
- [ ] Soglia spedizione gratuita ottimizzata
- [ ] Bundle key creati per categorie principali
- [ ] Prezzi "charm" applicati dove appropriato
- [ ] Conformità Direttiva Omnibus (prezzi barrati reali)
- [ ] Report margini mensile pianificato
- [ ] Dynamic pricing per stock basso configurato
