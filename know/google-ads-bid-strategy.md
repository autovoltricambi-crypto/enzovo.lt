# Google Ads — Strategie di Offerta (Bid Strategy)

## Panoramica Bid Strategy

La bid strategy determina come Google gestisce le tue offerte per raggiungere l'obiettivo. La scelta sbagliata può sprecare budget o limitare i risultati.

## Strategie Manuali

### CPC Manuale (Manual CPC)
Tu controlli ogni singola bid per keyword/prodotto.

**Quando usare:**
- Account nuovo con pochi dati
- Campagne con budget molto ristretto
- Keyword specifica su cui vuoi massimo controllo

**Contro:** richiede gestione continua, nessuna ottimizzazione AI.

### CPC Ottimizzato (Enhanced CPC — eCPC)
CPC Manuale + Google alza/abbassa la bid automaticamente in base alla probabilità di conversione.

**Quando usare:** transizione tra manuale e automatico.

## Strategie Automatiche — Conversioni

### Massimizza Conversioni
Google spende tutto il budget cercando il massimo numero di conversioni. Nessun target CPA.

**Quando usare:**
- Account con pochi dati di conversione (< 30/mese)
- Fase di lancio per raccogliere dati
- Budget fisso da spendere tutto

**Rischio:** può convertire a CPA molto alto se non monitorato.

### Target CPA (tCPA)
Google ottimizza per ottenere conversioni al costo target che imposti.

**Esempio:** Target CPA €15 → Google cerca di acquisire clienti spendendo in media €15/conversione.

**Quando usare:**
- Dopo aver accumulato 30-50 conversioni al mese
- Quando conosci il tuo CPA sostenibile

**Formula CPA sostenibile:**
```
Valore ordine medio × Margine % / Conversioni target = CPA massimo

Esempio:
Ordine medio: €80
Margine: 35%
→ Margine per ordine: €28
→ CPA max sostenibile: €10-15 (50-55% del margine)
```

### Target ROAS (tROAS)
Google ottimizza per raggiungere il ritorno sulla spesa pubblicitaria target.

**Esempio:** ROAS 400% → per ogni €1 speso, Google cerca di generare €4 di fatturato.

**Quando usare:**
- E-commerce con tracking valore ordine
- Dopo 50+ conversioni/mese
- Quando vuoi massimizzare il fatturato rispettando il margine

**Formula ROAS minimo:**
```
ROAS minimo = 1 / (Margine %)

Esempio con margine 30%:
ROAS minimo = 1 / 0.30 = 333%
→ Sotto 333% stai perdendo soldi sull'ads
→ Target ragionevole: 400-500%
```

### Massimizza Valore Conversioni
Spende tutto il budget massimizzando il valore (fatturato). Come "Massimizza Conversioni" ma ottimizza per valore, non numero.

## Strategie per Visibilità

### Target Quota Impressioni (Target Impression Share)
Appare in una % target delle aste.

**Utilizzo:** campagne brand — vuoi apparire SEMPRE quando cercano il tuo brand.
```
Target: 95% impression share
Posizione: Cima della pagina (assoluta)
```

### Massimizza Click
Spende il budget massimizzando i click, senza considerare conversioni.

**Quando usare:** campagne display o brand awareness, non performance.

## Portfolio Bid Strategies

Applica la stessa strategia a più campagne in un "portafoglio". Utile per:
- Campagne simili che condividono un target CPA/ROAS
- Stabilizzare le performance su campagne con pochi dati singolarmente

## Sequenza Consigliata per Account Nuovo

```
MESE 1-2: CPC Manuale o Massimizza Conversioni
→ Obiettivo: raccogliere dati di conversione (30-50/mese)

MESE 3-4: Target CPA
→ Imposta target conservativo (20% sopra CPA reale attuale)
→ Aggiusta gradualmente verso il target ideale

MESE 5+: Target ROAS (se tracking valore funziona)
→ Ottimizza per fatturato e margine
```

## Bid Adjustments (Modificatori Offerta)

Anche con Smart Bidding, puoi modificare le bid manualmente per:

| Segmento | Esempio | Quando alzare |
|----------|---------|---------------|
| **Dispositivo** | Mobile +20% | Se mobile converte bene |
| **Orario** | Sera +30% | Se le conversioni picco sera |
| **Giorno settimana** | Lunedì -20% | Se lunedì performa meno |
| **Geolocalizzazione** | Milano +15% | Se una città converte meglio |
| **Audience RLSA** | Visitatori +50% | Già conoscono il tuo sito |

**Nota:** con Smart Bidding (tCPA/tROAS), i bid adjustment vengono considerati come segnali, non applicati rigidamente.

## Errori Comuni

| Errore | Impatto | Soluzione |
|--------|---------|-----------|
| Cambiare strategia troppo spesso | Reset fase di apprendimento (7-14 giorni) | Aspetta almeno 2-4 settimane prima di cambiare |
| Target CPA troppo basso | Google non trova conversioni → impressioni crollano | Imposta target raggiungibile con +20% headroom |
| Target ROAS senza tracking valore | Ottimizza su dati sbagliati | Verifica sempre che il valore conversione sia corretto |
| Budget troppo basso per Smart Bidding | L'AI non ha abbastanza dati | Budget ≥ 10x CPA target al giorno |

## Fase di Apprendimento

Quando cambi strategia o aggiungi conversioni, Google entra in **"Fase di apprendimento"** (7-14 giorni):
- Performance instabile
- Non fare modifiche durante questo periodo
- È normale vedere CPA alto o basso erraticamente

## Checklist Bid Strategy

- [ ] Conversioni configurate e verificate in Google Ads
- [ ] Tracking valore ordine attivo (per tROAS)
- [ ] CPA sostenibile calcolato prima di impostare tCPA
- [ ] ROAS minimo calcolato prima di impostare tROAS
- [ ] Budget ≥ 10x CPA target/giorno
- [ ] Strategia corretta per la fase dell'account
- [ ] Nessuna modifica durante fase di apprendimento
