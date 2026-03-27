# SEO Locale

## Cos'è la SEO Locale

La SEO locale ottimizza la visibilità per ricerche geograficamente specifiche. Fondamentale se servi clienti in una zona specifica o vuoi targettizzare regioni italiane.

**Query locali:**
- "ricambi auto Milano"
- "ricambista BMW Torino"
- "filtri auto online Italia"

## Google Business Profile (GBP)

Il punto di partenza per qualsiasi SEO locale.

### Setup GBP

1. Vai su business.google.com
2. Crea/rivendica la tua attività
3. Verifica (cartolina, telefono, o video)
4. Completa TUTTI i campi

### Ottimizzazione Profilo

**Informazioni essenziali:**
```
Nome attività: enzovo.lt — Ricambi Auto Online
Categoria primaria: Negozio di ricambi auto
Categorie secondarie: Negozio di prodotti automobilistici, E-commerce
Indirizzo: [Se hai magazzino/ufficio]
Orari: Orari apertura (anche "Solo online 24/7" se applicabile)
Telefono: Numero di contatto
Sito web: enzovo.lt
Descrizione: 750 caratteri di descrizione con keyword
```

**Servizi:**
Aggiungi ogni tipo di ricambio come servizio:
- Filtri olio
- Pastiglie freno
- Kit tagliando
- Ammortizzatori
- ecc.

**Foto:**
- Logo aziendale
- Foto magazzino/ufficio (se presente)
- Foto prodotti
- Min 10 foto di qualità

### Post GBP

Pubblica regolarmente (1-2 volte/settimana):
- Nuovi prodotti arrivati
- Offerte stagionali
- Tips manutenzione
- Blog articles

**Tipi di post:**
- "Aggiornamento" → notizie, novità
- "Offerta" → promozioni con scadenza
- "Evento" → fiere, eventi
- "Prodotto" → prodotto specifico con link acquisto

### Recensioni Google

Le recensioni sono il fattore #1 per il ranking locale.

**Come ottenere più recensioni:**
1. Email automatica post-acquisto (giorno 10)
2. QR code nel packing slip che porta alla pagina recensioni
3. Link diretto: `https://g.page/r/[tuo_place_id]/review`
4. Chiedi verbalmente ai clienti soddisfatti

**Risposta alle recensioni:**
- Rispondi a TUTTE (positive e negative)
- Positive: ringrazzia e personalizza (non template)
- Negative: rispondi professionalmente, proponi soluzione offline

```
Recensione negativa:
"Ci dispiace per la tua esperienza. Il problema che descrivi è insolito
per noi — ti preghiamo di contattarci direttamente a info@enzovo.lt
così possiamo risolvere immediatamente."

Non: attacchi, scuse eccessive, toni difensivi
```

## NAP Consistency

**NAP = Name, Address, Phone**

Il tuo nome, indirizzo e telefono devono essere IDENTICI su:
- Google Business Profile
- Sito web (footer)
- Directory online (Pagine Gialle, Yelp)
- Social media
- Qualsiasi altra menzione online

**Anche piccole differenze (via vs viale, srl vs S.R.L.) confondono Google.**

## Citazioni Locali (Local Citations)

Directory dove listare la tua attività:

**Italiane:**
- Pagine Gialle (paginegialle.it)
- Virgilio
- TripAdvisor (per servizi con recensioni)
- Yelp Italia
- Indicatore.it

**Internazionali:**
- Bing Places
- Apple Maps
- Facebook Business
- LinkedIn Company Page
- Foursquare

**Settoriali auto:**
- Motorparts.it directory
- Forum auto (profilo utente)
- Associazioni ricambisti italiani

## SEO Locale On-Page

### Pagine Locali (Se Servi Zone Specifiche)

Se vuoi rankare per "ricambi auto [città]":
```
URL: /ricambi-auto-milano/
H1: "Ricambi Auto a Milano — Consegna il Giorno Dopo"
Contenuto: 400+ parole con menzioni città, zone, tempi consegna
Schema LocalBusiness con indirizzo
```

### Schema LocalBusiness

```json
{
  "@context": "https://schema.org",
  "@type": "AutoPartsStore",
  "name": "enzovo.lt",
  "url": "https://enzovo.lt",
  "telephone": "+39 XXX XXXXXXX",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "Via [...]",
    "addressLocality": "[Città]",
    "addressRegion": "[Provincia]",
    "postalCode": "[CAP]",
    "addressCountry": "IT"
  },
  "geo": {
    "@type": "GeoCoordinates",
    "latitude": "XX.XXXX",
    "longitude": "XX.XXXX"
  },
  "openingHours": "Mo-Fr 09:00-18:00",
  "priceRange": "€€"
}
```

Plugin Yoast SEO gestisce i dati strutturati → configura in Yoast → Conoscenza.

## Targeting Regionale su Google Ads

Per campagne ads localizzate:
- Campagna specifica per regione/città
- Copy con menzione città: "Ricambi BMW a Milano — Consegna Domani"
- Landing page con menzione location

## Local Pack (I 3 Risultati Locali)

Il "Local Pack" appare sopra i risultati organici per query locali.

**Fattori ranking Local Pack:**
1. Rilevanza (categoria GBP, parole chiave descrizione)
2. Distanza (dal ricercatore)
3. Prominenza (recensioni, link, autorità dominio)

**Per un e-commerce puro (senza sede fisica):** difficile apparire nel Local Pack per query geo-specifiche. Focus sulla SEO organica.

## Checklist SEO Locale

- [ ] Google Business Profile creato e verificato
- [ ] Tutti i campi GBP compilati
- [ ] Minimo 10 foto caricate
- [ ] Servizi aggiunti al profilo
- [ ] Schema LocalBusiness nel sito
- [ ] NAP consistente su tutti i canali
- [ ] Listato su Pagine Gialle, Bing Places, Apple Maps
- [ ] Sistema recensioni automatizzato
- [ ] Risposta a tutte le recensioni
- [ ] Post GBP almeno 1/settimana
