# Analytics — Modelli di Attribuzione

## Cos'è l'Attribuzione

L'attribuzione è il processo di assegnare credito per una conversione (acquisto) ai vari touchpoint che l'utente ha attraversato prima di comprare.

**Il problema:** un cliente potrebbe aver:
1. Visto un Reel Instagram
2. Fatto una ricerca Google (SEO)
3. Cliccato un Google Ad
4. Ricevuto un'email
5. Acquistato

Quale canale ha "causato" la vendita? La risposta dipende dal modello di attribuzione.

## Modelli di Attribuzione

### Last Click (Last Touch)
**100% del credito all'ultimo touchpoint prima dell'acquisto.**

```
Instagram → SEO → Google Ads → Email → ACQUISTO
                                        ↑
                              100% credito all'email
```

**Pro:** semplice, misura cosa ha "chiuso" la vendita.
**Contro:** ignora tutto il percorso precedente. Sovrastima email/brand.

**È il default di Google Ads** — quindi Google Ads sembra sempre molto efficace.

### First Click (First Touch)
**100% del credito al primo touchpoint.**

```
Instagram → SEO → Google Ads → Email → ACQUISTO
↑
100% credito a Instagram
```

**Pro:** capisce cosa ha generato la awareness iniziale.
**Contro:** ignora cosa ha convinto all'acquisto.

### Linear
**Credito distribuito equamente tra tutti i touchpoint.**

```
Instagram → SEO → Google Ads → Email → ACQUISTO
25%          25%     25%          25%
```

**Pro:** considera tutto il percorso.
**Contro:** non riflette l'importanza reale di ogni touchpoint.

### Time Decay
**Più credito ai touchpoint più vicini all'acquisto.**

```
Instagram → SEO → Google Ads → Email → ACQUISTO
5%           10%     25%          60%
```

**Pro:** premia ciò che ha "chiuso" ma considera il contesto.
**Contro:** sminuisce canali di awareness.

### Position Based (Data-Driven Alternativa)
**40% primo touchpoint, 40% ultimo, 20% al mezzo.**

```
Instagram → SEO → Google Ads → Email → ACQUISTO
40%           10%     10%          40%
```

**Pro:** equilibrio tra acquisition e conversion.
**Contro:** ignora la distribuzione reale.

### Data-Driven (Machine Learning)
**Google Ads/GA4 analizza tutti i percorsi e assegna credito basato su dati reali.**

Richiede: volume sufficiente (400+ conversioni/mese).

**Questo è il modello più accurato** — usalo quando hai dati sufficienti.

## Attribuzione in Google Analytics 4

GA4 usa **Data-Driven Attribution** di default.

**Dove visualizzarlo:**
Report → Pubblicità → Percorsi di conversione

**Cosa vedere:**
- Quali canali appaiono spesso come primo touchpoint?
- Quali canali chiudono le vendite?
- Quanto tempo passa tra primo touchpoint e acquisto?

### Confronto Modelli in GA4

**Come usarlo:**
Report → Pubblicità → Confronto modelli di attribuzione

Confronta: Last Click vs Data-Driven per ogni canale.

**Esempio interpretazione:**
```
Canale: Google Ads Search
Last Click: 45 conversioni (credito)
Data-Driven: 38 conversioni
→ Google Ads è leggermente sovrastimato in Last Click

Canale: SEO Organico
Last Click: 12 conversioni
Data-Driven: 28 conversioni
→ SEO è molto sottostimato in Last Click (svolge un ruolo importante ma non sempre chiude)
```

## Attribuzione Multi-Canale

### Il Problema della Duplicazione

Google Ads dice: "Ho generato 50 vendite".
Meta Ads dice: "Ho generato 40 vendite".
Email dice: "Ho generato 30 vendite".
→ Totale: 120 vendite. Ma ne hai fatte solo 80?

**Perché:** ogni piattaforma si attribuisce il merito con il suo modello (Last Click di default), e la stessa vendita viene contata da più canali.

**Soluzione:** guarda il totale delle vendite reali (WooCommerce), non la somma delle conversioni dei singoli canali.

### North Star Metric

Invece di guardare le conversioni per canale, guarda:

```
ROAS effettivo = Fatturato totale WooCommerce / Spesa totale ads

Se spendi €1.000 in ads e fai €8.000 di fatturato → ROAS reale 800%
Anche se Google Ads dice ROAS 600% e Meta dice ROAS 400%
(la somma è 1000%, ma è duplicazione)
```

## Customer Journey Analysis

### Tempo tra Prima Visita e Acquisto

Quanti giorni passano in media tra la prima visita e l'acquisto?

```
GA4: Report → Pubblicità → Percorsi di conversione → Lag report

Esempio risultato:
0 giorni: 40% degli acquisti (impulso)
1-7 giorni: 35%
8-30 giorni: 20%
30+ giorni: 5%

→ La maggior parte converte entro una settimana
→ L'attribution window di 7 giorni per le ads è corretta
```

### Touchpoint Medi Prima dell'Acquisto

```
1 touchpoint: 25% degli acquisti (hanno visto 1 cosa e comprato)
2-3 touchpoint: 40%
4+ touchpoint: 35%

→ Molti clienti richiedono più esposizioni
→ Il remarketing è fondamentale
```

## UTM Parameters — La Base del Tracking Multi-Canale

Aggiungi UTM a TUTTI i link che non vengono da Google/Meta:

```
Email newsletter:
https://enzovo.lt/filtri/bmw/?utm_source=email
  &utm_medium=newsletter&utm_campaign=weekly-2024-03&utm_content=filtri_bmw

Social media organico:
https://enzovo.lt/prodotto/filtro-olio-bmw-n47/
  ?utm_source=instagram&utm_medium=social&utm_campaign=organic_post

Influencer:
https://enzovo.lt/?utm_source=tiktok
  &utm_medium=influencer&utm_campaign=mario_meccanico_2024
```

**Tool:** Google Campaign URL Builder (gratuito, genera UTM automaticamente).

**In GA4:** vai a Report → Acquisizione → Acquisizione traffico → filtra per Sorgente/Mezzo.

## Attribuzione per Decisioni di Budget

### Come Usare l'Attribuzione per Allocare il Budget

```
Analisi percorsi:
SEO organico → appare nel 60% dei percorsi come primo touchpoint
Google Ads Search → chiude il 45% delle vendite
Email → presente nel 35% dei percorsi (middle)
Social organico → presente nel 20% dei percorsi

Decisione budget:
→ Investi in SEO (genera awareness)
→ Mantieni Google Ads (chiude le vendite)
→ Investi in email (nurturing efficace)
→ Social organico: mantieni ma non scalare con ads ancora
```

## Checklist Attribuzione

- [ ] GA4 con e-commerce enhanced configurato
- [ ] Data-Driven Attribution abilitata in GA4
- [ ] UTM parameters su tutti i link (email, social, influencer)
- [ ] Report "Percorsi di conversione" consultato mensilmente
- [ ] Confronto modelli attribuzione analizzato
- [ ] Budget allocato in base ai dati attribuzione (non solo Last Click)
- [ ] ROAS effettivo calcolato (fatturato WooCommerce / spesa totale ads)
- [ ] Lag report analizzato (tempo medio prima dell'acquisto)
