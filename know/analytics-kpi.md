# Analytics — KPI e Dashboard E-commerce

## KPI Fondamentali per E-commerce

### KPI di Acquisizione
Misurano quanto traffico arriva e da dove.

| KPI | Formula | Target |
|-----|---------|--------|
| **Sessioni** | Visite al sito | Crescita mensile |
| **Nuovi utenti** | Utenti nuovi / Totale | 60-70% |
| **CPA** | Costo totale ads / Acquisizioni | < LTV × 30% |
| **CAC** | Costo totale marketing / Nuovi clienti | < LTV × 33% |

### KPI di Coinvolgimento
Misurano quanto gli utenti interagiscono con il sito.

| KPI | Formula | Target E-commerce |
|-----|---------|------------------|
| **Bounce Rate** | Sessioni 1 pagina / Totale | < 40% |
| **Pagine per Sessione** | Pagine totali / Sessioni | > 3 |
| **Durata Sessione** | Secondi medi per sessione | > 2 minuti |
| **Scroll Depth** | % pagina scorsa | > 50% su prodotti |

### KPI di Conversione

| KPI | Formula | Target |
|-----|---------|--------|
| **Conversion Rate (CR)** | Acquisti / Sessioni × 100 | 1-4% |
| **Add-to-Cart Rate** | ATC / Sessioni × 100 | 5-15% |
| **Cart Abandonment** | 1 - (Acquisti / ATC) | < 70% |
| **Checkout Completion** | Acquisti / Checkout iniziati | > 60% |

### KPI di Monetizzazione

| KPI | Formula | Descrizione |
|-----|---------|-------------|
| **Fatturato** | Somma totale ordini | KPI principale |
| **AOV** | Fatturato / Numero ordini | Valore medio ordine |
| **RPV** | Fatturato / Sessioni | Revenue per visitatore |
| **Items per Ordine** | Item venduti / Ordini | Misura cross-sell |
| **Gross Margin** | (Fatturato - CoGS) / Fatturato | Margine lordo |

### KPI di Retention

| KPI | Formula | Target |
|-----|---------|--------|
| **Repeat Purchase Rate** | Acquirenti > 1 volta / Totale acquirenti | > 30% |
| **LTV** | AOV × Frequenza acquisti × Durata cliente | Dipende da settore |
| **Churn Rate** | Clienti persi / Clienti inizio periodo | < 15%/anno |
| **NPS** | % Promotori - % Detrattori | > 50 |

## Formula LTV (Customer Lifetime Value)

```
LTV = AOV × Frequenza annuale acquisti × Anni di relazione × Margine

Esempio:
AOV: €65
Frequenza: 2 acquisti/anno
Anni: 3 anni
Margine: 35%

LTV = €65 × 2 × 3 × 0.35 = €136.50

→ Puoi spendere fino a €45 per acquisire un cliente (33% LTV)
→ Campagne ads con CPA < €45 = profittevoli
```

## Dashboard KPI Mensile

### View Executive (CEO/Imprenditore)
```
Fatturato Mese: €X,XXX (+X% vs mese scorso)
Ordini: XXX (+X%)
AOV: €XX.XX
Nuovi Clienti: XXX
Clienti Ricorrenti: XX (XX%)
Top Canale: Organic/Paid/Email
Margine Lordo: XX%
```

### View Marketing
```
Traffico Totale: X,XXX sessioni
Organic: X,XXX (XX%)
Paid: XXX (XX%)
Email: XXX (XX%)
Social: XXX (XX%)

CR Sito: X.X%
ROAS Google Ads: XXX%
ROAS Meta Ads: XXX%
Email Revenue: €X,XXX
CAC: €XX
```

### View E-commerce
```
Top 10 Prodotti per Revenue
Top 10 Categorie per Revenue
CR per Categoria
AOV per Canale
Funnel Abbandono:
  - View Prodotto: 100%
  - Add to Cart: X%
  - Checkout: X%
  - Acquisto: X%
```

## Segmentazione dei Dati

Analizza sempre i dati per segmenti, non solo in aggregato:

### Per Canale
```
SEO: CR 2.3%, AOV €58
Google Ads: CR 3.1%, AOV €72
Email: CR 4.5%, AOV €81
Social Organic: CR 0.8%, AOV €45
Direct: CR 3.8%, AOV €90
```

### Per Dispositivo
```
Desktop: CR 3.2%, AOV €75
Mobile: CR 1.8%, AOV €58
Tablet: CR 2.5%, AOV €68

→ Mobile ha CR basso → opportunità CRO mobile
```

### Per Categoria Prodotto
```
Filtri: CR 3.5%, AOV €28
Freni: CR 2.8%, AOV €65
Sospensioni: CR 2.1%, AOV €120

→ Sospensioni CR bassa ma AOV alta → priorità CRO sospensioni
```

## Strumenti di Reporting

### Google Analytics 4 (Gratuito)
- Report standard
- Esplorazione personalizzata
- Audience per remarketing

### Looker Studio (ex Data Studio — Gratuito)
Dashboard visive condivisibili, collegabile a:
- GA4
- Google Ads
- Google Search Console
- Fogli Google
- MySQL/database

**Template pronti:** google.com/lookerstudio → Gallery template e-commerce.

### Fogli Google
Per tracking manuale e KPI settimanali/mensili:
```
= IMPORTDATA(url_ga4_export)
```

Oppure usa l'addon GA4 per Sheets.

## Anomaly Detection — Alert Automatici

Configura alert in GA4 per anomalie:

- Sessioni calate > 30% rispetto alla settimana scorsa
- Zero transazioni in 24 ore (potrebbe essere un bug)
- Bounce rate salito > 80% su una pagina specifica

**Dove configurare:** GA4 → Approfondimenti → Rileva anomalie (automatico con AI).

**Oppure:** integra con Slack via Google Apps Script per notifiche automatiche.

## Reporting Cadenza

| Report | Frequenza | Audience |
|--------|-----------|---------|
| KPI Flash | Giornaliero | Tu/team |
| Dashboard Performance | Settimanale | Marketing |
| Report Completo | Mensile | Business review |
| Analisi Trend | Trimestrale | Strategia |

## Checklist KPI

- [ ] GA4 con e-commerce enhanced configurato
- [ ] Tutti gli eventi tracciati correttamente
- [ ] Dashboard mensile creata (GA4 o Looker Studio)
- [ ] KPI definiti con target espliciti
- [ ] Confronto mese su mese configurato
- [ ] Segmentazione per canale attiva
- [ ] Alert anomalie configurati
- [ ] Review mensile KPI pianificata
- [ ] LTV calcolato per il proprio business
- [ ] CAC monitorato e confrontato con LTV
