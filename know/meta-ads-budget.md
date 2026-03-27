# Meta Ads — Budget, Bid Strategy e Scaling

## Struttura Budget Meta Ads

### CBO vs ABO

**CBO (Campaign Budget Optimization):**
Meta distribuisce il budget automaticamente tra i gruppi inserzioni.
```
Campagna Budget: €30/giorno
├── Gruppo A (Lookalike) → Meta gli dà €18/giorno (migliore performance)
├── Gruppo B (Interessi) → €8/giorno
└── Gruppo C (Retargeting) → €4/giorno
```

**Pro CBO:** Meta ottimizza meglio di noi, meno gestione.
**Contro CBO:** meno controllo su quale audience spende.

**ABO (Ad Set Budget Optimization):**
Budget fisso per ogni gruppo inserzioni.
```
Campagna (nessun budget)
├── Gruppo A: €20/giorno (garantito)
├── Gruppo B: €15/giorno
└── Gruppo C: €10/giorno
```

**Pro ABO:** controllo completo, utile per testare audience.
**Contro ABO:** non ottimizza in modo aggregato.

**Raccomandazione:**
- Test iniziale → ABO (budget garantito per ogni variante)
- Scale → CBO (Meta ottimizza verso i migliori)

## Bid Strategy

### Cost Per Result Goal (ex Lowest Cost)
Meta spende il budget con il CPA più basso possibile. Nessun target esplicito.

**Quando usare:** campagne nuove, poco storico, fase test.

### Bid Cap
Imposti il massimo che sei disposto a pagare per click/conversione.

**Quando usare:** quando vuoi limitare assolutamente il CPA.
**Rischio:** se il cap è troppo basso, Meta non spende il budget (non trova aste a quel prezzo).

### Cost Cap
Simile a Bid Cap ma funziona a livello di costo medio invece di massimo.

### Highest Volume (senza target)
Meta massimizza il numero di conversioni con il budget dato.

## Budget Iniziale per E-commerce

### Fase 1 — Test (Mese 1: €300-500)

```
Budget totale: €400/mese = €13/giorno

Distribuzione:
TOFU (acquisizione): €8/giorno
├── Campagna interessi auto: €8/giorno ABO

BOFU (retargeting): €5/giorno
└── Campagna carrello abbandonato: €5/giorno ABO
```

**Obiettivo:** raccogliere dati, capire cosa funziona, prime vendite.

### Fase 2 — Ottimizzazione (Mese 2-3: €500-800)

Dopo aver identificato le audience/creative migliori:

```
Budget: €700/mese = €23/giorno

TOFU: €13/giorno CBO
├── Gruppo Lookalike 1%
└── Gruppo Interessi auto vincente

BOFU: €10/giorno ABO
├── Carrello abbandonato 7gg: €6/giorno
└── Visitatori prodotti 14gg: €4/giorno
```

### Fase 3 — Scaling (Mese 4+: €1.000+)

```
Budget: €1.500/mese = €50/giorno

TOFU: €30/giorno
MOFU: €10/giorno
BOFU: €10/giorno
```

## Scaling Meta Ads

### Vertical Scaling (Aumentare Budget)

**Regola d'oro:** aumenta il budget del **10-20% ogni 3-4 giorni** (non raddoppiare di colpo).

```
Settimana 1: €10/giorno
Settimana 2: €12/giorno (+ 20%)
Settimana 3: €14/giorno
Settimana 4: €17/giorno
```

**Perché lentamente:** aumenti bruschi resettano la fase di apprendimento dell'algoritmo.

**Quando scalare:** ROAS stabile per 5+ giorni, CPA sotto il target.

### Horizontal Scaling (Nuove Audience)

Invece di aumentare il budget sulla stessa audience, crea nuove campagne/gruppi:

```
Attuale: Lookalike 1% from Clienti → ROAS 450%
Scale: Aggiungi Lookalike 2% (campagna separata)
Scale: Aggiungi Interessi diversi (campagna separata)
Scale: Lookalike 1% from Visitatori (campagna separata)
```

### Duplicate and Scale

Duplica un gruppo inserzioni performante con budget più alto:

```
Gruppo Originale: Lookalike 1% - €10/giorno - ROAS 500%
Duplicato 1: stesso targeting - €20/giorno
Duplicato 2: stesso targeting - €30/giorno
→ Mantieni l'originale, duplicati testano il nuovo budget
```

## Quando le Performance Calano

### Segnali di Deterioramento

- ROAS cala per 3+ giorni consecutivi
- CPP (Costo per Acquisto) aumenta > 30%
- CTR cala (audience satura)
- Frequenza alta (>3 in 7 giorni per una audience)

### Cause e Soluzioni

**Audience saturation:**
```
Problema: audience piccola, tutti hanno già visto l'annuncio
Soluzione: allarga audience (1% → 2-3% Lookalike) o cambia creatività
```

**Creative fatigue:**
```
Problema: stesse immagini/video da settimane
Soluzione: nuove creatività, stesso targeting
Regola: cambia creatività ogni 4-6 settimane
```

**Stagionalità:**
```
Problema: periodo naturalmente basso (estate, gen-feb)
Soluzione: riduci budget, non ottimizzare in eccesso
```

**iOS 14 / Problemi Tracking:**
```
Problema: meno conversioni tracciate = Meta ottimizza peggio
Soluzione: controlla Conversions API, deduplicazione
```

## Reporting e KPI Meta Ads

### Dashboard Settimanale

```
Spesa: €___
Acquisti: ___
Fatturato: €___
ROAS: ___x
CPP: €___
CTR: ___%
CPM: €___
Frequenza: ___
```

### Benchmark per Ricambi Auto

| KPI | Target |
|-----|--------|
| ROAS (totale) | > 300% |
| ROAS (retargeting) | > 500% |
| CPP | < 25% AOV |
| CTR Feed | > 1.5% |
| CPM | €6-12 |
| Frequenza (7gg) | < 3 (TOFU), < 7 (retargeting) |

## Attribution Window

**Impostazione raccomandata:**
- Click: 7 giorni
- View: 1 giorno (non 28 — troppo ottimista)

**Confronto con Google Ads:** Meta e Google possono attribuirsi la stessa conversione (se l'utente ha visto entrambi). Guarda il TOTALE delle vendite, non solo le conversioni segnalate dai singoli canali.

## Checklist Budget e Scaling

- [ ] CBO configurato per campagne mature
- [ ] ABO per test nuove audience
- [ ] Budget allocation: 60% TOFU, 20% MOFU, 20% BOFU
- [ ] Scaling: max +20% budget ogni 4 giorni
- [ ] Alert frequency cap (>3 su 7 giorni = azione)
- [ ] Creative refresh ogni 4-6 settimane
- [ ] Attribution window: 7 giorni click, 1 giorno view
- [ ] Confronto ROAS con obiettivo settimana su settimana
- [ ] Stop campagna se CPP > 30% AOV per 7+ giorni
