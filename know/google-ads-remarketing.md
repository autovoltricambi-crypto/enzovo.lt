# Google Ads — Remarketing

## Cos'è il Remarketing

Il remarketing (o retargeting) mostra annunci a persone che hanno già visitato il tuo sito. Sono i prospect più caldi — hanno già dimostrato interesse.

**Perché funziona:**
- L'utente medio visita 3-5 siti prima di comprare
- Il tasso di conversione di remarketing è 2-10x superiore al traffico freddo
- CPL/CPA più basso perché l'audience è già qualificata

## Tipi di Remarketing Google

### 1. Remarketing Display Standard
Mostra banner su milioni di siti della Google Display Network.

**Audience da creare:**
```
Visitatori ultimi 30 giorni → annunci generici
Visitatori pagina prodotto (non acquistato) → annunci prodotto specifico
Visitatori carrello abbandonato → annunci urgenza/sconto
Clienti esistenti → upsell/cross-sell
```

### 2. Remarketing Search (RLSA)
Modifica le bid per chi ha già visitato il sito quando cerca su Google.

```
Keyword: "filtro olio"
Se utente ha visitato il sito → bid +50% (sono più propensi a convertire)
Se utente è già cliente → bid +30% (fidelizzazione)
```

### 3. Remarketing Dinamico (per e-commerce)
Mostra automaticamente i prodotti che l'utente ha guardato sul sito.

**Requisiti:**
- Feed prodotti in Google Merchant Center
- Tag Google Ads con evento "view_item" / "add_to_cart"

**Esempio:** utente guarda "Filtro Olio BMW Elring" → vede banner con quella foto e prezzo esatto su altri siti.

### 4. Customer Match
Carica una lista di email di clienti esistenti → Google la matcha con account Google → mostra annunci a questi utenti specifici.

**Utilizzi:**
- Riattivare clienti inattivi (non comprano da 6+ mesi)
- Cross-sell a clienti che hanno comprato categoria X
- Escludere clienti recenti dalle campagne di acquisizione

## Configurazione Tag Google Ads

Installa il Global Site Tag + eventi specifici:

```javascript
// Tag base (su tutte le pagine)
gtag('js', new Date());
gtag('config', 'AW-XXXXXXXXX');

// Evento view_item (pagina prodotto)
gtag('event', 'view_item', {
  'send_to': 'AW-XXXXXXXXX',
  'value': 12.50,
  'items': [{
    'id': 'ELRING-163810',
    'price': 12.50,
    'google_business_vertical': 'retail'
  }]
});

// Evento add_to_cart (aggiunta carrello)
gtag('event', 'add_to_cart', {...});

// Evento purchase (acquisto completato)
gtag('event', 'purchase', {
  'transaction_id': 'ORD-12345',
  'value': 45.90,
  'currency': 'EUR'
});
```

In WordPress/WooCommerce usa il plugin **Google Site Kit** o **WooCommerce Google Ads** per automatizzare.

## Finestre Temporali (Membership Duration)

Quanto tempo un utente rimane nell'audience:

| Audience | Durata consigliata | Motivo |
|----------|-------------------|--------|
| Visitatori generici | 30 giorni | Intenzione d'acquisto breve |
| Pagina prodotto | 30 giorni | Finestra decisione |
| Carrello abbandonato | 7-14 giorni | Urgenza alta |
| Acquirenti | 90-180 giorni | Cross-sell / upsell |
| Clienti VIP | 365 giorni | Fidelizzazione |

## Struttura Campagna Remarketing

### Fase 1: Carrello Abbandonato (ROI più alto)
```
Audience: visitatori /cart/ (non hanno completato acquisto) — 7 giorni
Bid strategy: Target CPA o CPC manuale alto
Annuncio: "Hai dimenticato qualcosa? Completa il tuo ordine"
CTA: sconto 5% o spedizione gratuita
```

### Fase 2: Visitatori Pagina Prodotto
```
Audience: visitatori prodotti specifici — 30 giorni
Escludi: chi ha già acquistato
Annuncio: immagine del prodotto visto + prezzo
CTA: "Ancora disponibile — Acquista ora"
```

### Fase 3: Visitatori Homepage/Categoria
```
Audience: visitatori generici — 14 giorni
Annuncio: brand awareness + offerta generica
CTA: "Scopri il catalogo ricambi"
```

## Sequenza Annunci (Ad Sequencing)

Mostra annunci diversi in sequenza temporale:
- **Giorno 1-3:** Annuncio reminder (hai guardato questo prodotto)
- **Giorno 4-7:** Annuncio con recensioni/social proof
- **Giorno 8-14:** Annuncio con urgenza/sconto
- **Dopo 14 giorni:** Esclusione (non sprecare budget su chi non converte)

## Creatività per Remarketing

**Display Banner:**
- Formati: 300x250, 728x90, 160x600, 300x600
- Usa HTML5 o immagini statiche
- Elemento visivo prodotto + prezzo + CTA chiara

**Testo annuncio remarketing:**
```
✓ "Completa il tuo ordine — Filtro Olio BMW ancora disponibile"
✓ "Torna su enzovo.lt — Spedizione gratuita oggi"
✗ "Clicca qui per comprare" (troppo generico)
```

## Esclusioni Importanti

- **Clienti recenti** (acquisto ultimi 30 giorni): escludi dalle campagne acquisizione
- **Pagine non rilevanti:** escludere visitatori solo di /blog/, /about/ se non mostrano intento commerciale

## Checklist Remarketing

- [ ] Global Site Tag installato su tutte le pagine
- [ ] Evento purchase configurato e verificato
- [ ] Audience carrello abbandonato (7 giorni)
- [ ] Audience visitatori prodotti (30 giorni)
- [ ] Audience clienti (180 giorni)
- [ ] Campagna remarketing dinamico con feed
- [ ] RLSA attivato sulle campagne Search
- [ ] Annunci display in tutti i formati standard
- [ ] Frequenza cap: max 5-7 impressioni/utente/giorno
