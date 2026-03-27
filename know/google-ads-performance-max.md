# Google Ads — Performance Max (PMax)

## Cos'è Performance Max

Performance Max è il tipo di campagna "tutto in uno" di Google Ads. Una singola campagna appare su tutte le reti Google: Search, Shopping, Display, YouTube, Gmail, Maps.

Google usa l'AI per ottimizzare automaticamente dove mostrare gli annunci, a chi e quando, in base all'obiettivo di conversione.

**Ha sostituito:** Smart Shopping (2022) e Local Campaigns.

## Come Funziona

1. Fornisci **asset**: testi, immagini, video, titoli
2. Fornisci **segnali di audience**: chi sono i tuoi clienti ideali
3. Google **testa automaticamente** le combinazioni migliori su tutte le reti
4. L'algoritmo **ottimizza** verso l'obiettivo (acquisti, ROAS target)

## Asset Richiesti

### Testi
- **Titoli:** 3-5 (max 30 caratteri) — minimo 3
- **Titoli lunghi:** 1-5 (max 90 caratteri)
- **Descrizioni:** 2-4 (max 90 caratteri) — minimo 2
- **Business name:** nome del sito/brand

### Immagini
| Formato | Proporzione | Uso |
|---------|-------------|-----|
| Quadrata | 1:1 (1200x1200) | Display, Gmail |
| Landscape | 1.91:1 (1200x628) | Display, YouTube |
| Portrait | 4:5 (960x1200) | Instagram-style |
| Logo quadrato | 1:1 | Branding |
| Logo landscape | 4:1 | Display |

### Video
- **Consigliato:** video YouTube da 15-30 secondi
- Se non fornito, Google genera video automaticamente dagli asset (qualità bassa)
- **Consiglio:** crea almeno 1 video di prodotto

### Feed Prodotti (per e-commerce)
Collega il feed Google Merchant Center alla campagna PMax. È il modo più efficace per e-commerce — Google mostrerà automaticamente i prodotti pertinenti come annunci Shopping.

## Segnali di Audience

I segnali sono **suggerimenti**, non limitazioni rigide. Google può mostrare gli annunci anche ad audience diverse se l'AI lo ritiene opportuno.

**Tipi di segnali:**
- **Lista clienti:** carica email/telefoni di clienti esistenti
- **Visitatori sito:** chi ha visitato specifiche pagine
- **Audience simili:** Google genera da clienti esistenti
- **Interessi e segmenti:** "auto appassionati", "bricolage meccanico"
- **Keyword:** suggerisci le keyword più rilevanti come segnale

## Struttura Consigliata per E-commerce

### Opzione A: Una Campagna PMax per categoria
```
PMax — Filtri
├── Asset Group: Filtri Olio (immagini filtri olio, testi specifici)
└── Asset Group: Filtri Aria (immagini filtri aria, testi specifici)

PMax — Freni
└── Asset Group: Pastiglie Freno

PMax — Brand
└── Asset Group: keyword brand
```

### Opzione B: Una Campagna PMax con più Asset Group
Più semplice ma meno controllo sui report.

## Listing Groups (per e-commerce con feed)

Dentro ogni asset group puoi suddividere i prodotti:
```
Tutti i prodotti
├── Categoria: Filtri Olio → bid/target specifico
├── Categoria: Pastiglie Freno → bid/target specifico
└── Tutto il resto → bid basso
```

## Esclusioni in PMax

### Keyword brand da escludere
Aggiungi keyword brand come negative a livello account o campagna per evitare che PMax "rubi" traffico dalle campagne Search brand.

### URL da escludere
- `/cart/`, `/checkout/`, `/my-account/` — pagine non prodotto
- Prodotti esauriti se non vuoi spendere su di essi

### Placement da escludere
Puoi escludere specifici siti display dalla rete Google.

## Reporting Limitato

PMax ha meno trasparenza rispetto alle campagne standard:
- Non puoi vedere le query di ricerca dettagliate (solo "insight" aggregati)
- Non puoi vedere dove appaiono gli annunci (placement)
- Pochi dati su quale asset funziona meglio

**Come ovviare:**
- Usa Search Terms Report (parziale) in "Insights"
- Collega GA4 per dati più granulari
- Analizza i prodotti dal feed shopping

## Budget e Bid Strategy

**Consigliato:** Target ROAS dopo aver accumulato dati.

**Sequenza:**
1. Lancia con **Massimizza conversioni** (nessun target)
2. Accumula 30-50 conversioni nel primo mese
3. Imposta **Target ROAS** (es. 400% se vuoi €4 per ogni €1 speso)

**Budget:** PMax necessita budget sufficiente per l'AI — minimo €20-30/giorno per risultati significativi.

## Confronto PMax vs Standard Shopping

| Aspetto | Standard Shopping | Performance Max |
|---------|-----------------|-----------------|
| Controllo | Alto | Basso |
| Reti | Solo Shopping/Search | Tutte le reti Google |
| Setup | Manuale | Semi-automatico |
| Reporting | Dettagliato | Limitato |
| Efficacia | Buona con gestione | Ottima con dati sufficienti |

**Raccomandazione:** usa PMax con feed prodotti per e-commerce con catalogo ampio. Mantieni campagne Search separate per keyword ad alta intensità.

## Checklist PMax

- [ ] Feed GMC collegato e aggiornato
- [ ] Almeno 15 immagini (diversi formati e proporzioni)
- [ ] Almeno 1 video (YouTube)
- [ ] Tutti i testi compilati al massimo
- [ ] Segnali audience configurati (lista clienti + visitatori)
- [ ] Listing groups segmentati per categoria/margine
- [ ] Keyword brand in negative a livello account
- [ ] Budget minimo €20/giorno
- [ ] Conversioni acquisto configurate e verificate
