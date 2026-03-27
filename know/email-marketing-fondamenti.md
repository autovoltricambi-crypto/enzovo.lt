# Email Marketing — Fondamenti

## Perché l'Email Marketing è Ancora Fondamentale

L'email marketing ha il ROI più alto di qualsiasi canale digitale: mediamente **€36-42 per ogni €1 investito** (DMA 2023).

**Vantaggi unici:**
- Possiedi il canale (non dipendi da algoritmi di piattaforme terze)
- Costo marginale bassissimo per contatto
- Altamente personalizzabile e automatizzabile
- Misurabile in modo preciso
- Clienti che si iscrivono sono già interessati

## Piattaforme Email Marketing

| Piattaforma | Prezzo | Best For |
|-------------|--------|----------|
| **Klaviyo** | Da €0 (500 contatti) | E-commerce, integrazione WooCommerce |
| **Mailchimp** | Da €0 (500 contatti) | Generale, facile |
| **ActiveCampaign** | Da €29/mese | Automazione avanzata |
| **Brevo (Sendinblue)** | Da €0 | Budget limitato, GDPR-first |
| **MailerLite** | Da €0 | Semplicità e prezzo |

**Raccomandazione per WooCommerce:** Klaviyo (integrazione nativa, segmentazione potente basata su comportamento d'acquisto).

## Metriche Fondamentali

| Metrica | Formula | Benchmark E-commerce |
|---------|---------|---------------------|
| **Open Rate** | Aperture/Invii | 15-25% |
| **Click Rate** | Click/Invii | 2-5% |
| **CTOR** | Click/Aperture | 10-20% |
| **Conversion Rate** | Acquisti/Click | 2-5% |
| **Unsubscribe Rate** | Disiscritti/Invii | < 0.5% |
| **Bounce Rate** | Email non consegnate | < 2% |
| **Revenue Per Email** | Fatturato/Email inviata | Variabile, ottimizza |

## Tipi di Email

### 1. Transazionali
Inviate automaticamente in risposta a un'azione dell'utente:
- Conferma ordine
- Aggiornamento spedizione
- Ricevuta pagamento
- Password dimenticata

**Open rate altissimo** (50-80%) perché l'utente le aspetta. Ottimo posto per cross-sell.

### 2. Automatizzate (Triggered)
Inviate automaticamente in base al comportamento:
- Benvenuto nuovo iscritto
- Carrello abbandonato
- Win-back cliente inattivo
- Post-acquisto (recensione, prodotti correlati)

### 3. Campagne (Broadcast)
Inviate manualmente a segmenti:
- Newsletter settimanale/mensile
- Promozioni stagionali
- Lancio nuovo prodotto
- Offerta flash

## Lista Email — Come Costruirla

### Lead Magnet per E-commerce Ricambi
- Guida PDF: "Guida al tagliando fai-da-te BMW"
- Sconto primo acquisto: "10% sul primo ordine"
- Lista compatibilità: "Tutti i ricambi per la tua auto — inserisci modello"
- Avviso disponibilità: "Avvisami quando torna disponibile"

### Punti di Acquisizione
- **Pop-up sito:** appare dopo 30 secondi o all'intento di uscita
- **Footer sito:** sempre visibile
- **Checkout:** "Ricevi offerte esclusive" (pre-spuntata)
- **Post-acquisto:** iscrizione automatica
- **Social:** link bio Instagram, post Facebook

### GDPR — Obbligatorio in Italia/UE
- Consenso esplicito (double opt-in raccomandato)
- Informativa privacy chiara
- Link disiscrizione in ogni email
- Diritto alla cancellazione garantito
- Non acquistare liste email (illegale + inefficace)

## Deliverability — Arrivare nella Inbox

L'email più bella è inutile se va nello spam.

### Configurazione tecnica
```
DNS Records obbligatori:
- SPF: "v=spf1 include:_spf.klaviyo.com ~all"
- DKIM: firma crittografica del dominio mittente
- DMARC: "v=DMARC1; p=quarantine; rua=mailto:..."
```

### Reputazione del mittente
- Usa sempre un dominio verificato (non Gmail/Yahoo per business)
- Mantieni open rate > 15% — cancella inattivi
- Non fare spam — invia solo a chi ha dato consenso
- Warming up: inizia con volumi bassi su liste nuove

### Best Practice Contenuto
- Evita parole spam: "GRATIS", "Clicca qui", "Urgente"
- Bilanciamento immagini/testo: non solo immagini (filtri spam)
- Link non rotti
- Test su email client diversi (Gmail, Outlook, Apple Mail)

## Struttura Email Efficace

```
OGGETTO (50 caratteri max)
→ La cosa più importante — determina se viene aperta

PREVIEW TEXT (85 caratteri)
→ Testo dopo l'oggetto nelle inbox mobile

HEADER
→ Logo + eventuale banner prodotto

BODY (il contenuto)
→ Testo principale con beneficio/offerta
→ Immagini prodotto
→ Elenco punti chiave

CTA BUTTON
→ Un bottone principale, chiaro, grande

FOOTER
→ Indirizzo fisico (obbligatorio legalmente)
→ Link disiscrizione (obbligatorio)
→ Link privacy policy
→ Social links
```

## Oggetto Email — Il Fattore Più Importante

**Formula che funzionano:**
```
Curiosità: "Perché il tuo filtro olio fa questo..."
Urgenza: "Ultimi 3 pezzi disponibili — Filtro BMW"
Personalizzazione: "[Nome], un ricambio per la tua BMW"
Benefit diretto: "Risparmia €23 sul prossimo tagliando"
Domanda: "Hai già cambiato il filtro dell'aria?"
Numero: "5 errori che rovinano il motore BMW"
```

**Test A/B oggetto:** invia 20% lista con versione A, 20% con versione B, dopo 4 ore invia la vincente al restante 60%.

## Checklist Fondamenti Email

- [ ] Piattaforma email scelta e configurata
- [ ] SPF, DKIM, DMARC configurati sul dominio
- [ ] Lista email con consenso esplicito (GDPR)
- [ ] Double opt-in attivato
- [ ] Flusso benvenuto configurato
- [ ] Flusso carrello abbandonato configurato
- [ ] Template email con brand identity
- [ ] Test su device diversi prima di ogni invio
