# Analytics — Google Analytics 4

## Cos'è GA4

Google Analytics 4 (GA4) è la versione attuale di Google Analytics, obbligatoria dal luglio 2023 (Universal Analytics è stato disattivato). Si basa su eventi invece che su sessioni — ogni interazione è un "evento".

**Differenze principali da UA:**
- Modello event-based (non session-based)
- Cross-device tracking (desktop + mobile unificati)
- Privacy-first (cookie-less per il futuro)
- Machine learning integrato
- Report più flessibili ma meno intuitivi

## Setup GA4 per WooCommerce

### 1. Creare la Proprietà GA4
- Google Analytics → Admin → Crea proprietà
- Scegli "GA4"
- Configura fuso orario (Europe/Rome) e valuta (EUR)

### 2. Installazione su WordPress
**Plugin raccomandato:** Google Site Kit (ufficiale Google) o "GA4 for WooCommerce".

**Oppure via GTM (Google Tag Manager) — approccio avanzato ma più flessibile.**

### 3. Configurare E-commerce Tracking

Il tracking e-commerce deve essere abilitato esplicitamente.

**In GA4:** Admin → Configurazione → E-commerce → Attiva

**In WooCommerce:** il plugin ufficiale "Google Listings & Ads" o "Site Kit" gestisce automaticamente gli eventi.

**Eventi e-commerce standard:**
```javascript
// GA4 Ecommerce Events (via GTM o plugin)

// Visualizzazione lista prodotti
gtag('event', 'view_item_list', {
  item_list_name: 'Filtri Olio',
  items: [{ item_id: 'ELRING-163810', item_name: 'Filtro Olio BMW N47' }]
});

// Visualizzazione prodotto
gtag('event', 'view_item', {
  currency: 'EUR', value: 12.50,
  items: [{ item_id: 'ELRING-163810', price: 12.50 }]
});

// Aggiunta al carrello
gtag('event', 'add_to_cart', { currency: 'EUR', value: 12.50, items: [...] });

// Inizio checkout
gtag('event', 'begin_checkout', { currency: 'EUR', value: 45.90, items: [...] });

// Acquisto
gtag('event', 'purchase', {
  transaction_id: 'ORD-12345',
  value: 45.90,
  tax: 7.65,
  shipping: 0,
  currency: 'EUR',
  items: [...]
});
```

## Report Fondamentali per E-commerce

### Report Acquisizione
**Dove trovare:** Acquisizione → Acquisizione traffico

Mostra da dove arrivano i visitatori:
- Organic Search (SEO)
- Paid Search (Google Ads)
- Social (Facebook, Instagram)
- Email
- Referral (altri siti)
- Direct

**Metriche da guardare:** sessioni, conversioni, tasso di conversione, fatturato per canale.

### Report Monetizzazione
**Dove trovare:** Monetizzazione → Acquisti e-commerce

- **Panoramica:** fatturato, acquisti, AOV, items per ordine
- **Articoli e-commerce:** quali prodotti vendono di più
- **Transazioni:** lista ordini

### Funnel di Conversione
**Dove trovare:** Monetizzazione → Funnel di acquisto

Mostra dove gli utenti abbandonano nel processo:
```
Vista prodotto → Aggiungi carrello → Inizio checkout → Acquisto

Es:
1000 → Vista prodotto
300 → Aggiungi carrello (30% - abbandono 70%)
150 → Inizio checkout (50% - abbandono 50%)
90 → Acquisto (60% - abbandono 40%)

Opportunità: checkout ha abbandono 40% → ottimizza checkout
```

### Report Esplorazione (Exploration)
Report personalizzati avanzati:

**Funnel libero:**
Crea il tuo funnel con gli eventi che vuoi analizzare.

**Percorso utente:**
Visualizza il percorso degli utenti pagina per pagina.

**Sovrapposizione segmenti:**
Confronta comportamenti di segmenti diversi.

## Dimensioni e Metriche Chiave

### Dimensioni (Chi/Cosa)
- `item_name` — nome prodotto
- `item_category` — categoria prodotto
- `source/medium` — canale acquisizione
- `device_category` — desktop/mobile/tablet
- `country`, `city` — geo
- `landing_page` — prima pagina vista

### Metriche (Quanto)
- `sessions` — sessioni
- `users` — utenti unici
- `conversions` — conversioni
- `purchase_revenue` — fatturato
- `transactions` — numero ordini
- `average_order_value` (AOV)
- `ecommerce_purchases`

## Segmenti e Audience

GA4 permette di creare segmenti basati su:
- Comportamento sul sito
- Caratteristiche demografiche
- Sequenza di eventi

**Audience utili:**
- Visitatori pagina prodotto senza acquisto → esporta in Google Ads per remarketing
- Acquirenti con AOV > €100 → analisi comportamento
- Utenti mobile che abbandonano checkout → ottimizza UX mobile

**Esporta Audience in Google Ads:**
Admin → Link → Google Ads → Puoi usare segmenti GA4 come audience negli Ads.

## Google Search Console Integration

Collega GSC a GA4:
Admin → Link → Search Console

Aggiunge dati organici a GA4:
- Keyword che portano traffico
- Click, impressioni, CTR organico

## Configurazione Avanzata

### User ID (Cross-Device Tracking)
Se gli utenti si loggano sul sito, puoi inviare un User ID per tracciare lo stesso utente su più dispositivi.

WooCommerce con utenti registrati → configura User ID nel plugin GA4.

### Custom Dimensions
Aggiungi dati non standard:
```
Dimensione personalizzata: "marca_auto" → valore: "BMW"
Dimensione personalizzata: "tipo_ricambio" → valore: "filtri"
```

Utile per analisi specifiche del tuo business.

### Data Retention
GA4 conserva i dati per default 2 mesi. **Cambia a 14 mesi:**
Admin → Dati → Conservazione dati → 14 mesi.

### Filtri IP
Escludi il tuo IP (ufficio, casa) dai dati per non inquinare le statistiche.
Admin → Flussi dati → Configura tag → Lista indirizzi da non monitorare.

## Dashboard Personalizzata

Crea una dashboard semplice con le metriche chiave quotidiane:

```
Blocchi consigliati:
1. Sessioni oggi vs ieri vs settimana scorsa
2. Acquisti e fatturato oggi
3. Canali di acquisizione (torta)
4. Prodotti più venduti oggi
5. Paesi/città con più traffico
6. Dispositivi (mobile vs desktop)
```

**Tool alternativo:** Looker Studio (gratuito, si connette a GA4) per dashboard più belle e condivisibili.

## Checklist GA4

- [ ] Proprietà GA4 creata con fuso orario e valuta corretti
- [ ] Plugin installato e misurazione attiva
- [ ] E-commerce Enhanced configurato
- [ ] Tutti gli eventi e-commerce tracciati (view_item, add_to_cart, purchase)
- [ ] Valore transazione corretto (fatturato effettivo)
- [ ] GSC collegato
- [ ] Google Ads collegato
- [ ] Data retention impostata a 14 mesi
- [ ] IP interni esclusi
- [ ] Funnel di acquisto configurato nell'Esplorazione
- [ ] Alert configurati per anomalie (calo traffico, zero conversioni)
