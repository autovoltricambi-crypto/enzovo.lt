# Descrizioni Prodotto — Ricambi Auto

## Struttura Base di una Descrizione

Ogni prodotto deve avere:
1. **Titolo** — marca + tipo ricambio + compatibilità principale
2. **SKU** — codice articolo univoco (vedi sezione dedicata)
3. **Descrizione breve** (per anteprima) — 1-2 righe, beneficio principale
4. **Descrizione completa** — dettagli tecnici + compatibilità + note montaggio

---

## SKU Prodotto — Formato e Regole

Lo SKU è il codice articolo univoco nel sistema WooCommerce. Va compilato sempre.

### Formato SKU
```
[CODICE_FORNITORE]
```

Lo SKU è il codice del fornitore/ricambista — **solo il codice, senza la marca**.
La marca va nel titolo, non nello SKU.

**Esempi corretti:**
- SKU: `23.438.00` → Titolo: "Filtro Olio UFI BMW Serie 3 2.0d N47"
- SKU: `C26110` → Titolo: "Filtro Aria Mann Fiat Punto 1.4 Natural Power"
- SKU: `KTB459` → Titolo: "Kit Distribuzione Dayco Fiat 1.3 Multijet 16V"
- SKU: `FO101S` → Titolo: "Filtro Olio Japanparts Toyota Yaris 1.0 1.3"

**Regole SKU:**
- Sempre `[MARCA MAIUSCOLO]-[codice fornitore originale]`
- Usare il codice fornitore esatto, inclusi punti e trattini (`23.438.00` non `23438`)
- Non usare il codice OE casa costruttrice come SKU (quello va nei metadati)
- Non inventare codici — usare sempre il codice del catalogo fornitore
- Il campo `related_sku_code` in WooCommerce serve per codici interni Tecnocar (R304, OP400, ecc.) — non confonderlo con lo SKU

### SKU vs altri codici
| Campo | Esempio | Uso |
|-------|---------|-----|
| SKU WooCommerce | `23.438.00` | Codice fornitore — solo il codice, senza marca |
| Attributo "Marca ricambio" | `UFI` | Marca del ricambio — va come attributo WooCommerce, non nel SKU |
| Codice OE | `11427566327` | Codice originale casa costruttrice — per ricerca e SEO |
| related_sku_code | `R304` | Codice interno Tecnocar — solo per uso interno |

---

## Formula Titolo

```
[Marca] [Tipo Ricambio] [SKU] [Auto/Motore principale]
```

**Esempi corretti:**
- "Filtro Olio UFI 23.438.00 BMW Serie 3 2.0d N47"
- "Filtro Aria Mann C26110 Fiat Punto 1.4 Natural Power"
- "Kit Distribuzione Dayco KTB459 Fiat 1.3 Multijet 16V"
- "Filtro Carburante Japanparts FO101S Toyota Yaris 1.0 1.3"

**Regole titolo:**
- Sempre marca del ricambio (UFI, Mann, Mahle, Japanparts, ecc.)
- Sempre tipo prodotto leggibile (Filtro Olio, Filtro Aria, Kit Distribuzione)
- Sempre SKU (codice fornitore)
- Sempre auto + motorizzazione principale
- No codici interni (no "R304", no "OP400")
- Max 70 caratteri

---

## Formula Descrizione Breve

La descrizione breve deve sempre iniziare con il **tipo di prodotto** in italiano,
seguito da marca, veicolo di riferimento e codice OE se spazio.

```
[Tipo ricambio] [marca] di qualità OEM per [auto] con motore [motorizzazione].
Codice OE: [codice]. [Eventuale nota qualità].
```

**Esempio:**
> Filtro olio a vite UFI di qualità OEM per BMW Serie 3 con motore 2.0d N47 (2005–2012).
> Certificazione ISO 9001. Sostituzione diretta dell'originale BMW 11427566327.

---

## Formula Descrizione Completa

### Sezione 1 — Descrizione Prodotto
```
[Tipo ricambio] [marca] per [auto]. Prodotto di primo equipaggiamento equivalente,
garantisce le stesse prestazioni del ricambio originale.
[Caratteristiche tecniche: dimensioni, materiali, filtrazione se filtro, ecc.]
```

### Sezione 2 — Compatibilità Veicoli
> ⚠️ La compatibilità (marca auto, modello, anno, motorizzazione) è gestita
> automaticamente dal **plugin compatibilità WooCommerce** — vedi `plugin-compatibilita.md`.
> Non scrivere manualmente la lista veicoli nella descrizione del testo.
> Il plugin la visualizza in un tab dedicato della scheda prodotto.

Nella descrizione completa menzionare solo il veicolo/motore principale (1-2 righe)
come contesto, non l'elenco completo delle compatibilità.

### Sezione 3 — Codici di Riferimento
```
Codice OE (originale): [codice]
Codice articolo: [SKU prodotto]
Codici equivalenti: [altri codici cross-reference]
```

### Sezione 4 — Note di Montaggio (opzionale)
```
Sostituire ogni [km/mesi]. Verificare il corretto serraggio.
[Eventuali note tecniche specifiche.]
```

---

## Esempi Completi per Tipo Prodotto

### Filtro Olio a Vite (spin-on)

**Titolo:** Filtro Olio UFI BMW Serie 3 2.0d N47

**Descrizione breve:**
> Filtro olio a vite UFI per BMW Serie 3 E90/E91/E92/E93 con motore 2.0d N47 (2005–2012). Sostituzione OEM, filtraggio ad alta efficienza.

**Descrizione completa:**
> Filtro olio a vite UFI di qualità primo equipaggiamento per BMW Serie 3 con motore diesel 2.0d N47. Garantisce una filtrazione ottimale delle impurità nel circuito olio motore, proteggendo i componenti interni dall'usura.
> Compatibile con BMW Serie 3 (E90/E91/E92/E93) e Serie 1 (E81/E87) con motore N47.
> *(Lista completa compatibilità gestita dal plugin — vedi tab Compatibilità)*
>
> **Codici di riferimento:**
> - Codice OE BMW: 11427566327
> - Codice articolo (SKU): 23.438.00
>
> Intervallo di sostituzione consigliato: ogni 15.000 km o 12 mesi.

---

### Filtro Aria

**Titolo:** Filtro Aria Mann Fiat Punto 1.4 Natural Power

**Descrizione breve:**
> Filtro aria Mann per Fiat Punto III 1.4 Natural Power (2005–2012). Carta filtrante ad alta capacità, installazione diretta senza modifiche.

**Descrizione completa:**
> Filtro aria Mann di qualità OEM per Fiat Punto III con motore 1.4 8V benzina/metano. Garantisce un'ottimale filtrazione dell'aria in ingresso al motore, riducendo consumo di carburante e usura.
> *(Lista completa compatibilità gestita dal plugin — vedi tab Compatibilità)*
>
> **Codici di riferimento:**
> - Codice OE Fiat: 46479703
> - Codice articolo (SKU): C26110
>
> Sostituire ogni 30.000 km o 24 mesi.

---

### Kit Distribuzione

**Titolo:** Kit Distribuzione Dayco Fiat 1.3 Multijet 16V

**Descrizione breve:**
> Kit distribuzione completo Dayco per tutti i motori Fiat 1.3 Multijet 16V. Include cinghia, tenditore e rullo. Qualità OEM.

**Descrizione completa:**
> Kit distribuzione completo Dayco per motore Fiat 1.3 Multijet 16V (199A2, 199A3, 199B1, 263A2). Include:
> - Cinghia di distribuzione Dayco HPX (alta resistenza termica)
> - Tenditore automatico
> - Rullo rinvio
>
> *(Lista completa compatibilità gestita dal plugin — vedi tab Compatibilità)*
>
> **Codici di riferimento:**
> - Codice OE Fiat: 71753180
> - Codice articolo (SKU): KTB459
>
> Sostituzione consigliata ogni 120.000 km o 8 anni.

---

## Regole Generali

### DA FARE ✅
- Compilare sempre lo **SKU** con il solo codice fornitore (es. `23.438.00`, `C26110`)
- Includere il codice OE (originale casa costruttrice) nella sezione "Codici di riferimento"
- Menzionare nel testo il veicolo/motore principale (1-2 righe di contesto)
- Menzionare il marchio del ricambio (UFI, Mann, Dayco, ecc.)
- Indicare l'intervallo di sostituzione consigliato
- Usare termini di ricerca naturali (es. "filtro olio BMW" non "filtro lubrificante")
- Per la lista completa compatibilità → usare il **plugin compatibilità** (vedi `plugin-compatibilita.md`)

### DA EVITARE ❌
- Descrizioni generiche senza compatibilità specifica
- Solo codici tecnici senza spiegazione
- Testo copiato dal fornitore identico per tutti i prodotti
- Codici interni (related_sku_code) nella descrizione pubblica
- Promesse non verificabili ("il migliore sul mercato")

---

## Lunghezze Consigliate

| Campo | Lunghezza / Formato |
|-------|---------------------|
| Titolo | 50–70 caratteri |
| SKU | Solo codice fornitore (es. `23.438.00`, `C26110`, `KTB459`) |
| Descrizione breve | 150–200 caratteri |
| Descrizione completa | 300–600 parole |

---

## Parole Chiave da Includere Naturalmente

Per ogni prodotto includere nella descrizione:
- Nome tipo ricambio (filtro olio, filtro aria, kit distribuzione...)
- Marca del ricambio (UFI, Mann, Mahle, Dayco, Japanparts...)
- Marca auto (BMW, Fiat, Volkswagen...)
- Modello auto (Serie 3, Punto, Golf...)
- Codice motore (N47, 1.3 Multijet, 2.0 TDI...)
- Codice OE originale
- Anno di produzione del veicolo
