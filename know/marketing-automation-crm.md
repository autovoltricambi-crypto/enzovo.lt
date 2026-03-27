# Marketing Automation — CRM e Gestione Clienti

## Cos'è un CRM

CRM (Customer Relationship Management) è un sistema per gestire tutte le interazioni con clienti e potenziali clienti. Centralizza dati, comunicazioni e storico acquisti in un unico posto.

**Dati che un CRM per e-commerce deve gestire:**
- Dati anagrafici (nome, email, telefono, indirizzo)
- Storico acquisti (quando, cosa, quanto)
- Comportamento sul sito (pagine viste, carrelli abbandonati)
- Ticket assistenza
- Comunicazioni email/SMS
- Segmento e tag (BMW owner, cliente VIP, inattivo)

## CRM per WooCommerce

### Opzione 1: Klaviyo (Email + CRM leggero)

Klaviyo è tecnicamente una piattaforma email ma ha funzionalità CRM:
- Profilo cliente con storico ordini
- Segmentazione avanzata
- Timeline di ogni interazione

**Ideale per:** e-commerce con focus email marketing.

### Opzione 2: HubSpot CRM (Gratuito)

HubSpot CRM è gratuito e include:
- Gestione contatti illimitata
- Pipeline deals
- Email tracking
- Integrazione WooCommerce (plugin HubSpot)

**Ideale per:** vuoi un CRM vero ma non vuoi spendere.

### Opzione 3: ActiveCampaign

CRM + Email Marketing + Automazione in un'unica piattaforma.
- Contatti con scoring
- Pipeline vendita
- Automazioni avanzate
- Integrazione WooCommerce nativa

**Ideale per:** automazione avanzata + CRM.

### Opzione 4: WooCommerce + Plugin Nativi

Per iniziare, WooCommerce stesso ha:
- Lista clienti con storico ordini
- Filtri per data acquisto, valore ordine, prodotto acquistato
- Export CSV per importare in altri sistemi

**Plugin utili:**
- WooCommerce Customer History
- Customer Relationship Manager for WooCommerce

## Dati CRM per Ricambi Auto

### Profilo Cliente Ideale

```json
{
  "nome": "Marco Rossi",
  "email": "marco.rossi@email.it",
  "telefono": "+39 333 1234567",

  "auto": {
    "marca": "BMW",
    "modello": "Serie 3",
    "versione": "E90",
    "anno": 2008,
    "motore": "2.0d N47",
    "targa": "AB123CD"
  },

  "storico_acquisti": [
    {"data": "2024-03-15", "prodotto": "Filtro Olio Elring N47", "valore": 12.50},
    {"data": "2024-03-15", "prodotto": "Filtro Aria Mann", "valore": 14.90}
  ],

  "ltv": 87.40,
  "aov": 43.70,
  "ordini": 2,
  "ultimo_acquisto": "2024-03-15",
  "giorni_inattivo": 45,

  "segmenti": ["bmw_owner", "bmw_n47", "cliente_attivo"],
  "score": 75
}
```

### Come Raccogliere i Dati Auto

**Al checkout:** campo "Modello veicolo" (es. select menu o testo libero)
```
Campo opzionale: "Per quale auto stai comprando? (es. BMW Serie 3 2.0d 2008)"
→ Salva come metadato ordine → importa in CRM/Klaviyo come proprietà
```

**Da immatricolazione targa:** integrazione con API targa italiana per pre-compilare marca/modello.

**Da categoria prodotto:** se acquista filtro BMW → tag automatico "bmw_owner".

## Pipeline di Vendita (Funnel CRM)

```
LEAD (ha lasciato email)
  ↓ Welcome flow email
PROSPECT (ha visitato prodotti)
  ↓ Remarketing + nurturing
OPPORTUNITÀ (ha aggiunto al carrello)
  ↓ Carrello abbandonato automation
CLIENTE (ha acquistato)
  ↓ Post-purchase + cross-sell
CLIENTE FEDELE (2+ ordini)
  ↓ Loyalty program + referral
AMBASSADOR (raccomanda ad altri)
  ↓ Referral program
```

## Scoring Clienti

Assegna punteggi automatici per prioritizzare l'attenzione:

```python
# Logica scoring cliente

score = 0

# Recency (quando ha acquistato l'ultima volta)
if giorni_da_ultimo_acquisto < 30:
    score += 30
elif giorni_da_ultimo_acquisto < 90:
    score += 15
elif giorni_da_ultimo_acquisto < 180:
    score += 5

# Frequency (quante volte ha acquistato)
score += min(numero_ordini * 10, 30)

# Monetary (quanto ha speso in totale)
if ltv > 200: score += 30
elif ltv > 100: score += 20
elif ltv > 50: score += 10

# Engagement email
if apre_email: score += 10
if clicca_email: score += 15

# Segmento
if "bmw_owner": score += 5  # target audience

# Range: 0-100
# 70+: VIP → priorità assistenza, accesso early offers
# 40-70: Attivo → nurturing standard
# 20-40: A Rischio → win-back
# <20: Inattivo → soppressione
```

## Assistenza Clienti Integrata nel CRM

### Ticket System

Ogni richiesta di assistenza → ticket nel CRM:
```
Ticket #1234
Cliente: Marco Rossi (BMW E90)
Data: 2024-04-10
Problema: "Il filtro che ho ordinato non è compatibile"
Stato: Aperto
Urgenza: Alta

Storico ordini: [vedere profilo]
SLA: Risposta entro 4 ore
```

**Tool:**
- HubSpot Service Hub (gratuito base)
- Freshdesk (gratuito fino a 10 agenti)
- Zendesk (a pagamento, più completo)
- Tidio (chat + ticketing, ottimo per WooCommerce)

### Risposta Standard Problemi Comuni

**Problema compatibilità:**
```
"Ciao [Nome],

Ho verificato il tuo ordine #[numero]. Capisco il problema.

Dopo aver controllato le specifiche del prodotto e la tua [marca/modello],
[il prodotto è compatibile / ti invio il prodotto corretto].

[Soluzione specifica]

Fammi sapere se hai altre domande.
[Nome] — Assistenza enzovo.lt"
```

**Ritardo spedizione:**
```
"Ciao [Nome],

Il tuo ordine #[numero] è partito dal nostro magazzino il [data].
Tracking: [link]

Purtroppo c'è un leggero ritardo dovuto a [motivo].
Previsto entro [data].

Se non arriva entro [data+2], contattami e ti rimborso le spese di spedizione.

[Nome]"
```

## GDPR e Gestione Dati Clienti

### Obblighi Legali

**Consenso:** base legale per usare i dati (consenso esplicito o contratto per ordine).

**Dati da conservare:**
- Dati ordine: obbligatorio per 10 anni (fiscale)
- Email marketing: solo con consenso, fino a revoca
- Comportamentale (Pixel, cookie): con consenso cookie banner

**Diritti dell'utente:**
- Accesso ai propri dati
- Rettifica
- Cancellazione ("diritto all'oblio")
- Portabilità

**Cookie banner:** conforme GDPR con opzione di rifiuto granulare.
**Plugin WordPress:** Cookiebot, Complianz, GDPR Cookie Compliance.

### Data Retention Policy

```
Dati clienti attivi: mantenuti
Dati clienti inattivi (>5 anni): anonimizzati
Email marketing inattivi (>2 anni senza apertura): rimossi dalla lista
Log ordini: 10 anni (obbligo fiscale)
```

## Checklist CRM

- [ ] CRM scelto e configurato (anche WooCommerce base)
- [ ] Integrazione WooCommerce ↔ CRM attiva
- [ ] Dati auto del cliente raccolti al checkout
- [ ] Scoring clienti configurato
- [ ] Tag automatici per comportamento d'acquisto
- [ ] Pipeline CRM definita
- [ ] Sistema ticket assistenza attivo
- [ ] SLA di risposta definiti (es. < 4 ore)
- [ ] Template risposte standard create
- [ ] Privacy policy aggiornata (GDPR)
- [ ] Cookie banner conforme GDPR
- [ ] Data retention policy documentata
