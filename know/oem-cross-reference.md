# Codici OEM e Cross-Reference — Guida Operativa

## Cos'è un Codice OEM

OEM (Original Equipment Manufacturer) = codice del pezzo originale usato dal costruttore.
Ogni veicolo ha pezzi con codici OEM specifici assegnati dal costruttore (Fiat, BMW, VW, ecc.).

**Esempio concreto:**
- BMW usa il codice OEM `11 42 7 566 327` per il filtro olio dei motori N47 (2.0 diesel)
- Questo è il codice "originale" — qualsiasi filtro olio compatibile deve fare riferimento a questo

---

## Cross-Reference: Come Funziona

Lo stesso ricambio viene prodotto da più aziende aftermarket. Ognuna ha il suo codice:

| Tipo | Marca | Codice | Note |
|------|-------|--------|------|
| OEM | BMW | 11 42 7 566 327 | Originale costruttore |
| OES | Mahle | OX 387D | Fornitore originale BMW |
| IAM | Mann | HU 816 x | Aftermarket indipendente |
| IAM | UFI | 25.037.00 | Aftermarket indipendente |
| IAM | Purflux | L365 | Aftermarket indipendente |
| IAM | Bosch | F 026 407 123 | Aftermarket indipendente |

**Tutte queste sono lo stesso pezzo** → stesso `related_sku_code` nel nostro sistema.

---

## Dove Trovare i Codici OEM

### 1. Portali B2B (più affidabili)
- **AZ Car B2B** → nella scheda prodotto c'è la sezione cross-reference
- **Elring, Corteco, Valeo** → cataloghi online con ricerca per codice OE

### 2. Siti pubblici
- **TecDoc** (tecalliance.net) — database standard mondiale ricambi → cross-reference completi
- **AutoDoc.it** — nelle schede prodotto mostra "Codici OE compatibili"
- **Ricambio24.it**, **MisterAuto.it** — spesso hanno cross-reference

### 3. Cataloghi marca aftermarket
- Mann-Filter.com → ha lookUp per codice OE
- UFI Filters → catalogo online con cross-reference
- Mahle Aftermarket → catalogo con equivalenze

---

## Come Usare gli OEM nelle Descrizioni Prodotto

Quando aggiorni la descrizione di un prodotto su WooCommerce, includi SEMPRE gli OEM:

```html
<h3>Codici di Riferimento</h3>
<p><strong>Codice OE:</strong> 11 42 7 566 327</p>
<p><strong>Compatibile con:</strong> Mann HU 816 x, Mahle OX 387D, UFI 25.037.00, Purflux L365</p>
```

**Perché è fondamentale per la SEO:**
- Le persone cercano su Google il codice OEM del pezzo che devono sostituire
- "11427566327" ha volume di ricerca → ogni prodotto con quel codice nella descrizione si posiziona
- Più codici cross-reference = più parole chiave = più traffico organico

---

## Workflow: Aggiungere OEM ai Prodotti

1. Identifica il `related_sku_code` (es: R304)
2. Cerca il codice OE originale tramite portale B2B o web
3. Cerca i cross-reference (codici aftermarket equivalenti)
4. `cerca_prodotti_per_related_sku("R304")` → trova tutti i prodotti
5. Per ogni prodotto, aggiorna la descrizione includendo OEM e cross-reference
6. Usa `aggiorna_descrizioni_bulk` per fare tutto in batch
7. Crea un CSV di riferimento con `esporta_csv` per tenere traccia degli OEM trovati

---

## Formati Codici per Marca Auto

| Marca | Formato tipico OEM | Esempio |
|-------|-------------------|---------|
| BMW | XX XX X XXX XXX | 11 42 7 566 327 |
| Fiat/Alfa/Lancia | XXXXXXXXX | 55197218 |
| Volkswagen/Audi | XXX XXX XXX X | 03L 115 562 |
| Mercedes | XXX XXX XX XX | 651 180 01 09 |
| Ford | XXXXXXXX | 1717510 |
| Renault | XXXXXXXXXX | 8200768913 |
| Peugeot/Citroën | XXXXXXXXXX | 1109AY |
| Toyota | XX-XXX-XXXXX | 04152-YZZA1 |
| Hyundai/Kia | XXXXX-XXXXX | 26300-35503 |

Queste info servono per riconoscere e formattare correttamente i codici OEM.
