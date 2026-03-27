# Google Ads — Quality Score

## Cos'è il Quality Score

Il Quality Score (QS) è un punteggio da 1 a 10 che Google assegna ad ogni keyword. Influenza direttamente:

1. **Ad Rank** (posizione dell'annuncio)
2. **CPC effettivo** (quanto paghi per click)

**Formula Ad Rank:**
```
Ad Rank = Bid × Quality Score × Soglia × Contesto

→ Un QS alto ti permette di pagare MENO per la stessa posizione
→ QS 8 con bid €0.50 può battere QS 4 con bid €1.20
```

## I 3 Componenti del Quality Score

### 1. CTR Atteso (Peso Maggiore)
Probabilità che l'annuncio venga cliccato per quella keyword, rispetto alla media.

**Valori:** "Superiore alla media", "Nella media", "Inferiore alla media"

**Come migliorare:**
- Keyword esatta nel titolo dell'annuncio
- Annuncio pertinente alla query
- Estensioni che aumentano visibilità (sitelink, callout)
- Testare varianti RSA per trovare copy migliore

### 2. Rilevanza dell'Annuncio
Quanto l'annuncio corrisponde all'intento della keyword.

**Come migliorare:**
- Keyword nel titolo 1 dell'annuncio
- Keyword nella descrizione
- Evita gruppi annunci con troppe keyword non correlate
- Usa DKI (Dynamic Keyword Insertion) con cautela

### 3. Esperienza sulla Landing Page
Google valuta la pagina di destinazione per rilevanza e UX.

**Come migliorare:**
- Landing page specifica per la keyword (non homepage)
- Keyword dalla ricerca presente nel testo della pagina
- Velocità caricamento ottimale (Core Web Vitals)
- Mobile-friendly
- Contenuto pertinente e utile

## Interpretare il Quality Score

| QS | Interpretazione | Azione |
|----|----------------|--------|
| 1-3 | Critico | Riscrivi annunci, cambia landing page |
| 4-6 | Nella media | Ottimizza componenti deboli |
| 7-8 | Buono | Piccoli miglioramenti |
| 9-10 | Ottimo | Mantieni e scala |

## QS e Risparmio CPC

| QS | Modifica CPC rispetto a QS 6 |
|----|------------------------------|
| 10 | -50% |
| 9 | -44% |
| 8 | -37% |
| 7 | -28% |
| 6 | Base |
| 5 | +22% |
| 4 | +67% |
| 3 | +133% |

**Esempio pratico:**
```
Keyword "filtro olio BMW"
Bid: €1.00

QS 8 → CPC effettivo ~€0.63
QS 4 → CPC effettivo ~€1.67

Risparmio annuale con QS 8 vs QS 4 su 10.000 click:
(€1.67 - €0.63) × 10.000 = €10.400
```

## Strategia per Migliorare il QS

### Step 1: Identifica le keyword con QS basso
Colonna QS in Google Ads (devi aggiungerla manualmente alla vista).

Filtra: QS ≤ 5 + Impressioni > 100.

### Step 2: Analizza i 3 componenti
Per ogni keyword con QS basso, guarda quale componente è "Inferiore alla media".

### Step 3: Intervieni sul componente debole

**CTR Atteso basso:**
```
- Riscrivi i titoli RSA includendo la keyword esatta
- Aggiungi più estensioni
- Testa copy diversi (urgenza, beneficio, prezzo)
```

**Rilevanza Annuncio bassa:**
```
- Sposta la keyword in un gruppo annunci dedicato
- Crea annunci specifici per quella keyword
- Usa DKI: {KeyWord:Filtro Olio BMW}
```

**Esperienza Landing Page bassa:**
```
- Crea landing page dedicata (non mandare alla homepage)
- Inserisci la keyword nel titolo H1 della pagina
- Migliora velocità (GTmetrix, PageSpeed Insights)
- Assicurati che il prodotto/servizio cercato sia immediatamente visibile
```

## Quality Score per Campagne Shopping

Shopping non ha QS visibile, ma Google usa un concetto simile basato su:
- Qualità e completezza del feed (titoli, immagini, attributi)
- Landing page experience
- CTR storico del prodotto
- Prezzo competitivo rispetto ai competitor

## Account-Level Quality Score

Il QS storico dell'account influenza le nuove campagne:
- Account con storico positivo → QS iniziali più alti
- Account con molte keyword QS basso → più difficile lanciare nuove campagne

**Consiglio:** elimina keyword con QS 1-2 che non convertono — migliorano la salute generale dell'account.

## Checklist Quality Score

- [ ] Visualizzare colonna QS in Google Ads
- [ ] Identificare keyword con QS < 5 + > 100 impressioni
- [ ] Per ogni keyword: controllare quale componente è debole
- [ ] Gruppi annunci tematici (poche keyword correlate per gruppo)
- [ ] RSA con keyword nel titolo 1
- [ ] Landing page specifica per ogni tema principale
- [ ] Velocità landing page ottimale
- [ ] Estensioni complete e pertinenti
