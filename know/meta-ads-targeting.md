# Meta Ads — Targeting e Audience

## Tipi di Audience

### 1. Audience Principale (Core Audience)
Targeting per caratteristiche demografiche e interessi.

**Parametri disponibili:**
- **Demografici:** età, sesso, posizione geografica, lingua
- **Interessi:** categorie di interesse (auto, meccanica, fai da te)
- **Comportamenti:** acquirenti online, utenti di dispositivi specifici
- **Connessioni:** follower pagina, amici di follower

### 2. Custom Audience (Audience Personalizzate)
Audience basate su dati tuoi.

| Sorgente | Descrizione |
|----------|-------------|
| **Lista clienti** | Email/telefoni caricati da CRM/WooCommerce |
| **Traffico sito** | Visitatori tramite Pixel |
| **Engagement app** | Utenti app mobile |
| **Video** | Chi ha guardato X% di un video |
| **Instagram/Facebook** | Chi ha interagito con il profilo |
| **Lead form** | Chi ha compilato un form nativo |

### 3. Lookalike Audience (Audience Simili)
Meta trova persone simili a un'audience seme (seed).

**Come funziona:**
1. Fornisci seed audience (es. lista clienti)
2. Meta analizza i pattern
3. Crea audience di persone "simili" in Italia

**Percentuale Lookalike:**
- **1%** = più simile al seed, audience più piccola (alta qualità)
- **5%** = meno simile, audience più grande
- **10%** = molto meno simile, reach massimo

**Seed raccomandate per e-commerce:**
```
Clienti acquirenti (LTV alto) → Lookalike 1% → più preziosa
Visitatori pagina prodotto (30gg) → Lookalike 2%
Carrello abbandonato (30gg) → Lookalike 2%
```

## Targeting per Interessi — Ricambi Auto

**Interessi rilevanti:**
```
Categoria: Auto e veicoli
- Meccanica auto
- Auto fai da te (DIY)
- Tuning auto
- Marche auto: BMW, Fiat, Volkswagen
- Riviste: Quattroruote, AutoMoto
- Concessionari auto
- Accessori auto

Comportamenti:
- Acquirenti online recenti
- Engagement con contenuto auto
```

**Combinazioni audience:**
```
Interessi auto + Comportamento acquirenti online + Italia + 25-54 anni
→ Audience stimata: 500k - 2M (buon range)
```

## Broad Targeting (Advantage+ Audience)

Meta consiglia sempre di più il **targeting ampio** (Advantage+ Audience), lasciando che l'AI trovi la giusta audience automaticamente.

**Quando funziona:** campagne conversion con molti dati Pixel (50+ acquisti/settimana).

**Rischio per account nuovi:** Meta non ha abbastanza dati → risultati imprevedibili.

**Raccomandazione:** inizia con targeting specifico, passa a broad dopo aver accumulato dati.

## Audience Sizing

**Troppo piccola (< 50k):**
- Costi alti (CPM elevato)
- Frequenza alta rapidamente
- Poco spazio per ottimizzazione AI

**Ottimale (100k - 2M per conversioni):**
- Equilibrio tra qualità e scalabilità
- Spazio per ottimizzare

**Troppo grande (> 10M):**
- Difficile convertire efficacemente
- Spreco di budget su audience non rilevante

## Esclusioni Audience

Sempre escludere:
- **Clienti recenti** (ultimi 30gg) dalle campagne acquisizione → non sprecare budget
- **Audience BoFu da campagne ToFu** → evita sovrapposizioni
- **Paesi non serviti** → se spedisci solo in Italia, escludi tutto il resto

**Come escludere clienti recenti:**
1. Crea Custom Audience: "Acquirenti ultimi 30gg"
2. In ogni gruppo inserzioni → sezione Esclusioni → aggiungi quella audience

## Sovrapposizione Audience

Meta Ads Manager → Strumenti → Sovrapposizione Audience.

Se due audience si sovrappongono > 20%, stanno competendo tra loro (auction overlap) → unifica o segmenta meglio.

## IDFA e iOS 14 — Impatto sul Targeting

Post iOS 14.5 (2021), gli utenti iPhone possono bloccare il tracking:
- Meno dati Pixel disponibili
- Custom audience da sito più piccole
- Pixel riporta meno conversioni (underreporting tipicamente 20-40%)

**Soluzioni:**
- **Aggregated Event Measurement:** configura in Events Manager
- **Conversions API:** dati server-side non bloccati da iOS
- **Modeled Conversions:** Meta stima le conversioni non tracciate

## Segmentazione per Funnel

```
TOFU — Acquisizione
Audience: Interessi auto + Lookalike clienti 2-5%
Esclusioni: visitatori sito 30gg
Budget: 60% del totale

MOFU — Consideration
Audience: Visitatori sito 30gg (non acquistato)
Esclusioni: acquirenti
Budget: 20%

BOFU — Retargeting
Audience: Carrello abbandonato 7gg + Prodotto visto 14gg
Esclusioni: acquirenti recenti 30gg
Budget: 20%
```

## Checklist Targeting

- [ ] Custom Audience: visitatori sito per diversi periodi (7, 30, 90gg)
- [ ] Custom Audience: carrello abbandonato
- [ ] Custom Audience: acquirenti (da lista email WooCommerce)
- [ ] Lookalike 1% da clienti acquirenti
- [ ] Lookalike 2% da visitatori prodotto
- [ ] Interessi auto definiti per TOFU
- [ ] Esclusioni configurate in ogni gruppo inserzioni
- [ ] Audience size controllata (100k-2M per conversioni)
