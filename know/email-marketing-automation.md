# Email Marketing — Automazione e Flussi

## Cos'è l'Email Automation

L'automazione invia email automaticamente in risposta a trigger (azioni, eventi, date). Una volta configurata, lavora 24/7 senza intervento manuale. È il modo più efficiente per monetizzare la lista email.

## I Flussi Fondamentali per E-commerce

### 1. Flusso Benvenuto (Welcome Series)
**Trigger:** nuova iscrizione alla newsletter

**Obiettivo:** presentare il brand, costruire fiducia, convertire al primo acquisto.

```
Email 1 (Immediata): Benvenuto + coupon promesso
→ "Ecco il tuo 10% di sconto"
→ Presenta il catalogo brevemente

Email 2 (Giorno 2): Chi siamo e perché ci differenziamo
→ "Perché enzovo.lt, non il concessionario"
→ Benefici: ricambi OES, prezzi, spedizione, assistenza

Email 3 (Giorno 5): Contenuto di valore
→ "Guida: come scegliere il filtro olio giusto per la tua auto"
→ Link a categorie prodotti rilevanti

Email 4 (Giorno 10): Scadenza coupon (urgenza)
→ "Il tuo sconto scade fra 48 ore"
→ Categorie bestseller

Condizione: SE ha acquistato → esci dal flusso
```

### 2. Flusso Carrello Abbandonato (Abandoned Cart)
**Trigger:** aggiunto prodotto al carrello ma non completato acquisto (1+ ora dopo)

**Il flusso più redditizio per e-commerce — recupera il 10-15% dei carrelli abbandonati.**

```
Email 1 (1 ora): Reminder gentile
Oggetto: "Hai dimenticato qualcosa?"
→ Mostra i prodotti nel carrello
→ Link diretto al checkout
→ Nessuno sconto (aspetta)

Email 2 (24 ore): Social proof + benefici
Oggetto: "Il tuo ordine ti aspetta — spedizione gratuita"
→ Recensioni sul prodotto abbandonato
→ Benefici: reso facile, assistenza, garanzia
→ Link checkout

Email 3 (72 ore): Incentivo
Oggetto: "Ultimo reminder: 5% di sconto solo per te"
→ Coupon sconto personale con scadenza 24h
→ Urgenza: "Disponibilità limitata"

Condizione: SE acquista tra email → esci dal flusso
```

### 3. Flusso Post-Acquisto
**Trigger:** ordine completato

```
Email 1 (Immediata): Conferma ordine
→ Dettagli ordine, numero tracking
→ "Grazie per il tuo acquisto"
→ Info spedizione

Email 2 (Giorno 2-3): Aggiornamento spedizione
→ Tracking link
→ Info su come installare il prodotto (valore aggiunto)

Email 3 (Giorno 7-10): Recensione
→ "Come valuti il tuo acquisto?"
→ Link a Google Reviews o Trustpilot
→ Offerta per ordine successivo

Email 4 (Giorno 30): Cross-sell
→ "Prodotti correlati per la tua BMW Serie 3"
→ Basato su cosa ha comprato
→ "Il filtro aria andrebbe cambiato con il filtro olio"
```

### 4. Flusso Win-Back (Riattivazione)
**Trigger:** cliente non acquista da 90+ giorni

```
Email 1 (Giorno 90): "Ci manchi!"
→ Mostra i loro acquisti precedenti
→ Novità nel catalogo

Email 2 (Giorno 105): Offerta esclusiva
→ "Sconto 15% per il tuo ritorno"
→ Validità 7 giorni

Email 3 (Giorno 115): Ultima chance
→ "Ultimo giorno per il tuo sconto"
→ Se non risponde → sposta a lista "Inattivi"
```

### 5. Flusso Browse Abandonment
**Trigger:** visitato pagina prodotto ma non aggiunto al carrello (24 ore dopo)

```
Email 1: "Stai ancora pensando a [prodotto]?"
→ Immagine del prodotto visto
→ Recensioni prodotto
→ Disponibilità in tempo reale
```

### 6. Flusso Disponibilità (Back In Stock)
**Trigger:** prodotto torna disponibile dopo essere esaurito

```
Email: "Buone notizie! [Prodotto] è di nuovo disponibile"
→ Urgenza: "Quantità limitata"
→ CTA immediata
```

## Segmentazione nei Flussi

I flussi performano meglio se personalizzati per segmento:

```python
# Logica condizionale nel flusso

SE cliente.marca_auto == "BMW":
    mostra_prodotti = filtra_per_compatibilita("BMW")
    oggetto = f"Ricambi BMW per la tua {cliente.modello}"
ALTRIMENTI SE cliente.marca_auto == "Fiat":
    ...
```

**Segmenti da usare:**
- Marca auto (se raccolta al checkout o opt-in)
- Valore ordine (alto/medio/basso)
- Categoria acquistata (filtri, freni, sospensioni)
- Geografico (nord/sud Italia)

## Timing Ottimale per E-commerce Italia

| Email | Giorno | Orario | Note |
|-------|--------|--------|------|
| Newsletter | Martedì/Giovedì | 10:00 o 18:00 | Evita lunedì e venerdì |
| Promozione | Giovedì | 14:00 | Prima del weekend |
| Recap offerte | Domenica | 19:00 | Pianificazione settimana |

**Nota:** testa sempre sulla tua lista specifica — varia per audience.

## Smart Sending — Evitare Oversaturation

Klaviyo e ActiveCampaign hanno "Smart Sending":
- Non invia se l'utente ha già ricevuto un'email nelle ultime X ore
- Evita di bombardare un utente con 3 email in un giorno

**Configura:** finestra di 16-24 ore tra email dello stesso flusso.

## Metriche per Ottimizzare i Flussi

| Flusso | Open Rate Target | Conv Rate Target |
|--------|-----------------|-----------------|
| Welcome | 40-60% | 3-8% |
| Carrello Abbandonato | 35-50% | 5-15% |
| Post-Acquisto | 45-65% | 1-3% (cross-sell) |
| Win-Back | 15-25% | 2-5% |

## Checklist Automazione

- [ ] Flusso Benvenuto (3-4 email)
- [ ] Flusso Carrello Abbandonato (3 email con timing)
- [ ] Flusso Post-Acquisto (4 email)
- [ ] Flusso Win-Back (3 email)
- [ ] Browse Abandonment (1 email)
- [ ] Back In Stock (1 email)
- [ ] Smart Sending attivato
- [ ] Condizioni "esci se acquista" in ogni flusso
- [ ] Segmentazione per marca auto nei flussi principali
- [ ] Test A/B su oggetto in ogni flusso
