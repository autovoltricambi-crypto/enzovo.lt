# Marketing Automation — Fondamenti

## Cos'è il Marketing Automation

Il marketing automation è l'uso di software per automatizzare attività di marketing ripetitive: email, messaggi, post social, lead nurturing, segmentazione. Permette di comunicare con migliaia di contatti in modo personalizzato senza intervento manuale.

**Differenza:**
- **Email Marketing:** invii email manuali o automatizzate (1 canale)
- **Marketing Automation:** orchestrazione multi-canale (email + SMS + social + ads + CRM)

## Piattaforme

| Piattaforma | Prezzo | Punti Forza |
|-------------|--------|-------------|
| **Klaviyo** | Da €0 | E-commerce, WooCommerce nativo |
| **ActiveCampaign** | Da €29/mese | CRM + automazione avanzata |
| **HubSpot** | Da €0 (CRM) / €800 (Marketing) | All-in-one, B2B |
| **Mailchimp** | Da €0 | Semplice, generale |
| **Omnisend** | Da €16/mese | E-commerce, multi-canale |

**Per WooCommerce:** Klaviyo o Omnisend (integrazione nativa).

## Il Funnel di Marketing Automation

```
LEAD GENERATION (acquisizione contatti)
↓ Form sito, popup, social lead ads, checkout
↓

LEAD NURTURING (educazione e warming)
↓ Email sequenze, contenuto personalizzato
↓

LEAD SCORING (qualificazione automatica)
↓ Chi è più pronto all'acquisto?
↓

CONVERSIONE
↓ Offerta al momento giusto per il contatto giusto
↓

POST-CONVERSIONE
↓ Onboarding, upsell, cross-sell, retention
↓

REATTIVAZIONE
↓ Win-back clienti inattivi
```

## Trigger e Condizioni

### Trigger (cosa avvia l'automazione)

**Basati su tempo:**
- X giorni dopo iscrizione
- X giorni dopo acquisto
- Data specifica (compleanno, anniversario)

**Basati su comportamento:**
- Visitato pagina specifica
- Aperto email
- Cliccato link
- Aggiunto al carrello
- Completato acquisto

**Basati su proprietà:**
- Campo cambiato (es. "marca_auto" aggiornata a "BMW")
- Valore ordine superato soglia
- Tag aggiunto/rimosso

### Condizioni (biforcazioni IF/ELSE)

```
SE ha_acquistato = true
  → Flusso post-acquisto
ALTRIMENTI
  → Continua nurturing

SE marca_auto = "BMW"
  → Email con prodotti BMW
ALTRIMENTI SE marca_auto = "Fiat"
  → Email con prodotti Fiat
ALTRIMENTI
  → Email generica
```

### Azioni (cosa fa l'automazione)

- Invia email
- Invia SMS
- Aggiungi/rimuovi tag
- Aggiorna proprietà contatto
- Sposta a lista diversa
- Notifica team interno
- Aggiungi a campagna ads

## Lead Scoring

Assegna punteggi automaticamente in base alle azioni:

```
Azione → Punti
Apertura email → +2
Click email → +5
Visita pagina prodotto → +3
Aggiunta al carrello → +10
Acquisto completato → +25
Inattivo 30 giorni → -5
Disiscrizione email → -50
```

**Soglie:**
- 0-20: Lead freddo → nurturing automatico
- 21-50: Lead tiepido → automazione consideration
- 51+: Lead caldo → offerta diretta o contatto commerciale

## Automazioni Fondamentali per E-commerce

### 1. Welcome Flow (già dettagliato in email-marketing-automation.md)

### 2. Abandoned Cart Recovery
**Multi-canale:**
- Email 1h: reminder carrello
- SMS 24h: offerta urgenza
- Ads retargeting: costante per 7 giorni

### 3. Post-Purchase Sequence
- Email transazionale (conferma + tracking)
- Email assistenza (3 giorni)
- Email recensione (10 giorni)
- Email cross-sell (30 giorni)

### 4. Manutenzione Preventiva

Per ricambi auto, ogni ricambio ha una vita utile:
```
Cliente acquista "Filtro Olio BMW N47"
→ Tag: "filtro_olio_bmw_n47_acquistato_[data]"
→ Automazione: dopo 365 giorni → email "È ora del tagliando?"
→ Include prodotti dello stesso kit tagliando
```

### 5. Segmentazione Automatica

```
Trigger: acquisto completato
↓
IF prodotto.categoria == "filtri"
  → aggiungi tag "interessato_filtri"
  → avvia sequenza cross-sell filtri correlati

IF prodotto.marca_auto == "BMW"
  → aggiungi tag "bmw_owner"
  → inserisci in segmento BMW per future campagne
```

### 6. Reactivation Flow
```
Trigger: nessun acquisto da 90 giorni
↓
Email 1: "Ci manchi! Cosa stiamo facendo per te"
Aspetta 5 giorni → SE non apre → Email 2
↓
Email 2: Offerta esclusiva 10%
Aspetta 7 giorni → SE non acquista → Email 3
↓
Email 3: "Ultima email che ti mandiamo" (FOMO finale)
↓
SE non acquista → sposta a lista "Inattivi" → soppresso dalle email normali
```

## SMS Marketing Automation

SMS ha open rate del 98% vs 20% email. Ideale per:
- Conferma ordine
- Aggiornamento spedizione
- Offerte flash (24h)
- Reminder carrello abbandonato

**Piattaforme SMS Italia:** Twilio, Nexmo, SMSHosting.

**Normativa:** consenso esplicito + opt-out semplice ("Rispondi STOP").

```
Esempio SMS:
"enzovo.lt: Il tuo filtro BMW è spedito! Traccia: [link]
Per non ricevere SMS: rispondi STOP"
```

## Integrazione CRM + E-commerce

**Dati che fluiscono da WooCommerce a CRM:**
- Ogni ordine → crea/aggiorna contatto
- AOV, LTV, frequenza → aggiornati automaticamente
- Prodotti acquistati → tag automatici
- Carrelli abbandonati → trigger automazione

**Tool di integrazione:**
- Klaviyo: integrazione nativa WooCommerce
- Zapier: connette WooCommerce a qualsiasi CRM (HubSpot, Salesforce)
- WooCommerce Webhooks: eventi real-time verso sistema esterno

## Checklist Marketing Automation

- [ ] Piattaforma scelta e integrata con WooCommerce
- [ ] Welcome flow attivo (3-5 email)
- [ ] Abandoned cart flow attivo (3 email + eventuale SMS)
- [ ] Post-purchase flow attivo (4 email)
- [ ] Reactivation flow attivo (3 email)
- [ ] Segmentazione automatica per marca auto
- [ ] Segmentazione automatica per categoria acquistata
- [ ] Lead scoring configurato
- [ ] SMS per spedizione e ordine
- [ ] Review mensile performance automazioni
