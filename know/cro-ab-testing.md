# CRO — A/B Testing

## Cos'è l'A/B Testing

L'A/B test mostra due versioni di una pagina/elemento a due gruppi di utenti e misura quale converte meglio.

```
50% traffico → Versione A (originale/controllo)
50% traffico → Versione B (variante)

Vincitore: la versione con più conversioni (statisticamente significativa)
```

## Quando Fare A/B Testing

**Requisiti minimi:**
- Traffico sufficiente: almeno 200-500 conversioni/variante per risultati affidabili
- Durata minima: 2 settimane (per cicli settimanali completi)
- Una sola variabile cambiata per volta

**Se hai poco traffico:** fai invece "best practice implementation" senza test (applica direttamente i principi CRO consolidati).

## Cosa Testare (Priorità)

### Alto Impatto

**1. Bottone CTA:**
```
A: "Aggiungi al Carrello" (verde)
B: "Acquista Ora — Spedizione Gratis" (arancione)

Metriche: Add-to-Cart Rate
```

**2. Headline Pagina Prodotto:**
```
A: "Filtro Olio Elring 163.810"
B: "Filtro Olio BMW N47 — Compatibilità Garantita | Elring"
```

**3. Immagine Principale Prodotto:**
```
A: Immagine standard su bianco
B: Immagine prodotto installato su motore BMW
```

**4. Prezzo Visualizzato:**
```
A: €12.50
B: ~~€18.00~~ €12.50 (con prezzo barrato)
```

**5. Trust Badge:**
```
A: Nessun badge
B: Badge "SSL Sicuro | Reso Gratuito | Spedizione 24h" sotto CTA
```

### Medio Impatto

**Checkout — Numero di Passi:**
```
A: Checkout 3 pagine
B: Checkout 1 pagina (one-page checkout)
```

**Spedizione Gratuita Threshold:**
```
A: "Spedizione gratuita sopra €30"
B: "Spedizione gratuita sopra €35"
→ Misura: AOV e Revenue totale
```

**Pop-up Newsletter:**
```
A: "Iscriviti per le ultime offerte" (generico)
B: "10% di sconto sul primo ordine + guide gratis" (specifico)
```

### Basso Impatto (ma facili da testare)

- Colore bottone CTA
- Testo nel bottone
- Posizione del prezzo
- Numero recensioni mostrate

## Significatività Statistica

Il test è valido solo quando la differenza è statisticamente significativa.

**Obiettivo:** 95% di confidenza (p-value < 0.05)

**Calcolatore:** usa uno A/B test calculator online (Optimizely, VWO, AB Test Guide).

```
Esempio:
A: 500 visitatori, 15 conversioni → CR 3.0%
B: 500 visitatori, 21 conversioni → CR 4.2%

Differenza: +40%
Confidenza statistica: 87%
→ NON abbastanza (< 95%) → continua il test

Dopo altri 200 visitatori:
A: 600 visitatori, 18 conversioni → CR 3.0%
B: 600 visitatori, 28 conversioni → CR 4.7%

Confidenza: 96%
→ Significativo → B vince
```

## Tool per A/B Testing

### Gratuiti
**Google Optimize:** (terminato il servizio nel 2023)

**Growthbook (open source):** alternativa gratuita a Optimize.

**WordPress + plugin:**
- Nelio A/B Testing (a pagamento ma abbordabile)
- Simple Page Tester

### A Pagamento
- **Optimizely:** enterprise, molto potente
- **VWO (Visual Website Optimizer):** €170+/mese
- **AB Tasty:** €
- **Convert:** €

**Per siti WooCommerce piccoli:** inizia con Nelio A/B Testing o Growthbook.

## Implementazione Test

### Step 1: Definisci Ipotesi
```
"Aggiungendo badge di fiducia (SSL, reso, spedizione) sotto il bottone
Aggiungi al Carrello, il tasso di conversione aumenterà perché
riduce l'ansia pre-acquisto degli utenti."
```

### Step 2: Definisci Metrica Primaria
- Add-to-Cart Rate
- Conversion Rate (acquisto)
- Revenue per Visitor

**Non** monitorare 10 metriche — sceglila una primaria prima di iniziare.

### Step 3: Calcola Dimensione Campione

Prima di lanciare, calcola quanti visitatori ti servono:

```
AB Test Sample Size Calculator:
- CR baseline: 2%
- Minimum detectable effect: 20% (vuoi vedere se sale da 2% a 2.4%)
- Confidenza: 95%
- Potere statistico: 80%

→ Risultato: ~3.800 visitatori per variante
→ Se hai 500 visitatori/giorno → durata: 15 giorni
```

### Step 4: Lancia e Aspetta

**Non interrompere il test prematuramente** (anche se vedi subito una variante che sembra vincere).

I dati potrebbero essere influenzati da:
- Giorno della settimana (diverso comportamento lunedì vs weekend)
- Effetto novità (gli utenti cliccano sulla nuova versione per curiosità)
- Stagionalità

**Regola:** aspetta almeno 2 settimane complete.

### Step 5: Analizza e Decidi

**Variante B vince (95%+ confidenza):**
→ Implementa definitivamente B

**Nessun vincitore chiaro:**
→ Mantieni A (non modificare senza prova)
→ Formula nuova ipotesi più impattante

**Variante B perde:**
→ Interessante — perché non ha funzionato come previsto?
→ Analizza, impara, formula nuova ipotesi

## A/B Test Roadmap per E-commerce

### Priorità per Sito Nuovo

```
Sprint 1 (Mese 1-2):
- Test CTA button: testo e colore
- Test trust badges pagina prodotto
- Test headline categoria principale

Sprint 2 (Mese 3-4):
- Test immagine hero homepage
- Test layout checkout
- Test spedizione gratuita threshold

Sprint 3 (Mese 5-6):
- Test upsell/cross-sell nel carrello
- Test personalizzazione per dispositivo
- Test social proof (posizione recensioni)
```

## Errori Comuni A/B Testing

| Errore | Problema | Soluzione |
|--------|---------|-----------|
| Interrompere troppo presto | Falso positivo | Rispetta la durata calcolata |
| Testare più variabili contemporaneamente | Non sai cosa ha causato il cambiamento | 1 variabile alla volta |
| Campione troppo piccolo | Risultati non affidabili | Calcola campione prima di iniziare |
| Ignorare la segmentazione | Risultati diversi per segmenti diversi | Analizza mobile vs desktop separatamente |
| Test durante eventi anomali | Black Friday distorce dati | Non testare durante promozioni grandi |

## Checklist A/B Testing

- [ ] Ipotesi formulata chiaramente
- [ ] Metrica primaria definita
- [ ] Dimensione campione calcolata
- [ ] Durata minima definita (almeno 2 settimane)
- [ ] Tool configurato e test lanciato
- [ ] Nessuna modifica durante il test
- [ ] Dati analizzati con calcolatore di significatività
- [ ] Decisione presa con 95%+ confidenza
- [ ] Risultato documentato (per imparare nel tempo)
- [ ] Prossima ipotesi già pronta
