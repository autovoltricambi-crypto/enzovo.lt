# CRO — Conversion Rate Optimization (Fondamenti)

## Cos'è la CRO

La CRO è il processo sistematico per aumentare la percentuale di visitatori che compiono un'azione desiderata (acquisto, iscrizione, ecc.) sul sito.

**Formula:**
```
Conversion Rate = (Conversioni / Visitatori) × 100

E-commerce: Acquisti / Sessioni totali × 100
```

**Benchmark e-commerce:**
- Media globale: 1-3%
- Buono: 3-5%
- Ottimo: 5%+

**Perché la CRO è fondamentale:**
Raddoppiare il tasso di conversione = raddoppiare il fatturato **senza aumentare il traffico**.

```
Scenario A: 10.000 visitatori × 1% CR × €60 AOV = €6.000/mese
Scenario B: 10.000 visitatori × 2% CR × €60 AOV = €12.000/mese
```

## Il Processo CRO

### 1. Raccolta Dati (Research)
Prima di testare, capisci dove e perché gli utenti abbandonano.

**Tool quantitativi:**
- Google Analytics 4: funnel di conversione, pagine di uscita
- Heatmap (Hotjar, Microsoft Clarity — gratuito): dove cliccano
- Session recording: guarda vere sessioni utente

**Tool qualitativi:**
- Sondaggi on-site: "Cosa ti ha impedito di completare l'acquisto?"
- Survey post-acquisto: "Come hai trovato il sito?"
- User testing: chiedi a qualcuno di comprare e osserva

### 2. Identificazione dei Problemi (Hypothesis)
Basandoti sui dati, identifica le cause di attrito.

**Esempi di problemi comuni:**
- Tasso di abbandono carrello del 75%? → Problema nel checkout
- Pagina prodotto con alto bounce? → Informazioni insufficienti o prezzo
- Form lungo → tasso completamento basso

### 3. Formulare Ipotesi
**Template:** "Cambiando X in Y, crediamo che Z migliorerà perché..."

```
"Aggiungendo badge di fiducia (SSL, pagamenti sicuri) vicino al bottone
'Acquista', crediamo che il tasso di conversione migliorerà del 10-20%
perché gli utenti sono preoccupati per la sicurezza dei pagamenti online."
```

### 4. Prioritizzazione (ICE Framework)
| Criteri | Descrizione | Punteggio 1-10 |
|---------|-------------|----------------|
| **Impact** | Quanto impatterà se funziona? | 8 |
| **Confidence** | Quanto sei sicuro che funzionerà? | 7 |
| **Ease** | Quanto è facile da implementare? | 9 |
| **ICE Score** | Media dei 3 | 8.0 |

Prioritizza le modifiche con ICE più alto.

### 5. Testing (A/B Test)
Testa solo **una variabile alla volta**. Vedi `cro-ab-testing.md`.

### 6. Implementazione e Iterazione
Se il test vince → implementa definitivamente → prossima ipotesi.
Se perde → analizza perché → nuova ipotesi.

## Principi Psicologici della Conversione

### Social Proof
Le persone seguono le scelte degli altri.
```
"⭐⭐⭐⭐⭐ 4.8/5 da 1.247 recensioni"
"Marco da Milano ha appena acquistato questo filtro"
"Prodotto più venduto della categoria"
```

### Scarcity e Urgency
La paura di perdere (FOMO) spinge all'azione.
```
"Solo 3 rimasti in magazzino"
"Ordina entro le 14:00 per ricevere domani"
"Offerta valida fino a domenica"
```

**Attenzione:** l'urgenza falsa distrugge la fiducia se scoperta.

### Rimozione dell'Attrito
Ogni passaggio aggiuntivo riduce le conversioni. Semplifica al massimo.
```
Checkout in 1 pagina vs 3 pagine → +20-35% conversioni
Guest checkout (senza registrazione) → +20% conversioni
Autofill indirizzo → riduce abbandono mobile
```

### Prova di Fiducia
Riduce l'ansia pre-acquisto, specialmente su siti meno conosciuti.
```
✓ SSL / Pagamenti sicuri (badge Visa, Mastercard, PayPal)
✓ Politica reso chiara (30 giorni soddisfatto o rimborsato)
✓ P.IVA e indirizzo fisico visibili
✓ Numero di telefono / chat dal vivo
✓ Recensioni verificate (Trustpilot, Google)
```

### Anchoring
Il primo prezzo visto diventa il riferimento.
```
Prezzo originale: €25,90 → OFFERTA: €18,90
→ L'utente percepisce un risparmio di €7
```

### Reciprocità
Dai valore prima di chiedere.
```
Guida gratuita → registrazione email → prima vendita
```

## Dove Agisce la CRO

### Gerarchia delle opportunità

1. **Checkout** → massimo impatto (ogni 1% migliorato = molti €)
2. **Pagina prodotto** → convincere chi è già interessato
3. **Pagina categoria** → orientare verso i prodotti giusti
4. **Homepage** → prima impressione e orientamento
5. **Form** → acquisizione lead, iscrizioni

## Metriche da Monitorare

| Metrica | Descrizione |
|---------|-------------|
| Conversion Rate | % visitatori che acquistano |
| Add-to-Cart Rate | % visitatori che aggiungono al carrello |
| Cart Abandonment Rate | % che abbandona il carrello |
| Checkout Completion Rate | % che completa il checkout |
| Average Order Value (AOV) | Valore medio ordine |
| Revenue Per Visitor (RPV) | Fatturato / Visitatori |

## Checklist Fondamenti CRO

- [ ] Google Analytics 4 con funnel e-commerce configurato
- [ ] Heatmap installata (Hotjar o Microsoft Clarity)
- [ ] Session recording attivo sulle pagine chiave
- [ ] Tasso di abbandono carrello misurato
- [ ] Sondaggio on-site configurato
- [ ] Lista ipotesi prioritizzate con ICE
- [ ] Processo A/B test definito
