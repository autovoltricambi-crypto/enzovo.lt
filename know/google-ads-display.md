# Google Ads — Display Network

## Cos'è la Display Network

La Google Display Network (GDN) è una rete di 2+ milioni di siti, app e video dove Google mostra i tuoi annunci banner. Raggiunge il 90% degli utenti Internet.

**Differenza rispetto a Search:**
- **Search:** utente cerca attivamente → alta intenzione
- **Display:** banner su siti che l'utente visita → bassa intenzione, alta copertura

**Uso principale per e-commerce:** remarketing e brand awareness (non acquisizione fredda diretta).

## Formati Annunci Display

### Responsive Display Ads (RDA)
Google genera automaticamente annunci da:
- 5 Titoli (max 30 char)
- 5 Descrizioni (max 90 char)
- 1-15 Immagini
- 1-5 Logo

Google combina automaticamente per adattarsi a ogni placement.

### Immagini Statiche (Upload)
Carica immagini nei formati standard:

| Formato | Dimensioni | Uso |
|---------|-----------|-----|
| Large Rectangle | 336x280 | Alta performance |
| Medium Rectangle | 300x250 | Più comune |
| Leaderboard | 728x90 | Header siti |
| Wide Skyscraper | 160x600 | Sidebar |
| Half Page | 300x600 | High impact |
| Large Mobile | 320x100 | Mobile |
| Billboard | 970x250 | Top of page |

**Formato file:** JPG, PNG, GIF animato (max 150KB).

### HTML5 Ads
Banner animati con interazione. Richiedono asset HTML5 → più costosi da produrre ma CTR più alto.

## Targeting Display

### Per Audience (Chi Vedere)
- **Custom Intent:** utenti che cercano keyword specifiche (es. "filtro olio BMW")
- **In-Market:** utenti che stanno valutando acquisti nella categoria
- **Affinity:** interesse a lungo termine (appassionati auto)
- **Remarketing:** chi ha già visitato il tuo sito
- **Customer Match:** lista email clienti
- **Lookalike:** simili ai tuoi clienti

### Per Placement (Dove Apparire)
- **Automatico:** Google sceglie dove
- **Siti specifici:** scegli siti manualmente (es. quattoruote.it)
- **Categorie:** siti di auto, meccanica, ecc.
- **App:** applicazioni mobile specifiche

### Per Contesto (Argomento della Pagina)
- **Keyword contestuali:** appare su pagine che contengono le tue keyword
- **Topic:** appare su pagine in una categoria specifica

## Campagna Display — Setup

### Obiettivi e Bid Strategy

**Brand Awareness:** Target CPM (costo per 1000 impressioni)
**Consideration:** Target CPA o Massimizza click
**Remarketing:** Target CPA

### Segmentazione Campagne

```
Campagna 1: Remarketing
→ Audience: visitatori sito 30gg
→ Bid: più alto (audience calda)
→ Creatività: prodotti specifici visti

Campagna 2: In-Market Auto
→ Audience: utenti in-market "Ricambi auto"
→ Bid: medio
→ Creatività: offerta generica brand

Campagna 3: Brand Awareness
→ Audience: Affinity "Appassionati auto"
→ Bid: CPM basso
→ Creatività: brand identity
```

## Brand Safety — Dove NON Apparire

Escludi sempre:
- Contenuto per adulti
- Contenuto violento
- Fake news
- App mobile (spesso traffico non qualificato)
- Placement irrilevanti

**Opzione:** "Inventario standard" o "Inventario limitato" nelle impostazioni campagna.

**Placement Exclusion List:** crea lista condivisa di siti esclusi da usare su tutte le campagne.

## Frequenza e Brand Recall

**Frequenza cap:** quante volte un utente vede il tuo annuncio al giorno.

- Awareness: 3-5 impressioni/utente/giorno
- Remarketing: 5-7 impressioni/utente/giorno
- Oltre 10/giorno: banner blindness, spreco budget

## View-Through Conversions

Le conversioni view-through si verificano quando:
1. Utente vede il tuo banner (ma NON clicca)
2. Poi visita il sito e acquista in una sessione successiva

Google le conta nel report → possono "gonfiare" le conversioni.

**Come gestire:** finestra view-through 1-7 giorni (non 30), considera le VTC solo come dato integrativo.

## Performance Creativa

### Headline Efficaci per Display
```
"Filtro BMW da €12.50 | Spedito Domani"
"Ricambi Auto Compatibili Garantiti"
"Tagliando BMW — Risparmia il 60%"
"Ordina Ora | Reso Gratuito 30gg"
```

### Design Banner
- Logo sempre visibile
- CTA button contrastante (non grigio)
- Testo leggibile (min 16px su 300x250)
- Immagine prodotto chiara
- Branding consistente tra tutti i formati

## Reporting Display

**Metriche chiave:**

| Metrica | Descrizione |
|---------|-------------|
| Impressions | Quante volte mostrato |
| CPM | Costo per 1000 impressioni |
| CTR | % click/impressioni (display: 0.1-0.3% è normale) |
| View-through Conv | Conversioni dopo aver visto (non cliccato) |
| Relative CTR | Tuo CTR vs media per quel placement |

**Dove ottimizzare:**
- Placement con alto costo e zero conversioni → escludi
- Audience con CTR molto basso → pausa o cambia creatività
- Creatività con CTR basso → sostituisci

## Display vs Remarketing Dinamico

| Aspetto | Display Standard | Remarketing Dinamico |
|---------|-----------------|---------------------|
| Targeting | Audience generica | Solo chi ha visitato |
| Creatività | Manuale | Auto (usa feed prodotti) |
| Intenzione audience | Bassa | Alta |
| CPA | Alto | Basso |
| Setup | Semplice | Richiede feed GMC |

**Per e-commerce:** prioritizza il remarketing dinamico sul display generico.

## Checklist Display

- [ ] Responsive Display Ads con 5 titoli, 5 descrizioni, 5+ immagini
- [ ] Immagini in tutti i formati standard caricati
- [ ] Brand safety configurata (inventario limitato)
- [ ] Placement exclusion list applicata
- [ ] Frequenza cap impostata
- [ ] Campagna remarketing separata da awareness
- [ ] View-through window impostata a 7 giorni
- [ ] Review placement mensile (esclusioni)
