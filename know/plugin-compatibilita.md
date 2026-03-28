# Plugin Compatibilità Veicoli — Guida Completa

## Come Funziona il Plugin

Il plugin permette ai clienti di selezionare la propria auto (marca/modello/motore)
e vedere SOLO i prodotti compatibili. Riduce i resi e aumenta la fiducia.

**3 elementi fondamentali:**
1. **Database veicoli** — archivio di marche, modelli, motorizzazioni
2. **Collegamento prodotti ↔ veicoli** — ogni prodotto è collegato ai veicoli compatibili
3. **Filtro intelligente** — mostra solo i prodotti giusti per l'auto selezionata

Il collegamento avviene tramite **import Excel/CSV** — non si inserisce a mano.
Il CSV usa il campo `related_sku_code` come chiave di collegamento.

---

## Il Sistema di Codici Interni (related_sku_code)

Il `related_sku_code` è un **codice interno** che identifica un ricambio
indipendentemente dalla marca. Serve a raggruppare prodotti identici di
marche diverse (cross-reference) e a collegarli al CSV di compatibilità veicoli.

### Struttura dei Codici per Categoria

**Filtri Aria** → prefisso `A`
```
A2181, A2183, A2190 ...
(riferimento catalogo Tecnocar)
```

**Filtri Olio** → due serie:
```
OP → filtri a bagno (cartuccia): OP400, OP246, OP312 ...
R  → filtri a vite (spin-on):    R304, R100, R520 ...
```

**Filtri Carburante** → due serie:
```
N  → a bagno:  N311, N290 ...
RN → a vite:   RN260, RN180 ...
```

---

## SKU vs related_sku_code — Differenza Fondamentale

Sono due campi DISTINTI e non devono essere confusi:

| Campo | Scopo | Esempio |
|-------|-------|---------|
| `sku` | Codice univoco del prodotto (marca specifica) | `UFI-23.438.00` |
| `related_sku_code` | Codice interno cross-reference del ricambio | `R304` |

**Un prodotto ha UN solo SKU ma può condividere il related_sku_code con altri prodotti di altre marche.**

---

## Cross-Reference — Esempio Pratico

Il filtro olio R304 esiste in due marche:

```
Prodotto 1:
  nome: "Filtro Olio UFI"
  sku: "UFI-23.438.00"
  prezzo: €8.50
  related_sku_code: "R304"    ← stesso codice

Prodotto 2:
  nome: "Filtro Olio Japanparts"
  sku: "FO-022JM"
  prezzo: €7.20
  related_sku_code: "R304"    ← stesso codice
```

Nel CSV di compatibilità veicoli:
```
R304 → compatibile con: Fiat Punto 1.3 MJT, Fiat Panda 1.3 MJT, ...
```

→ Il plugin collega AUTOMATICAMENTE entrambi i prodotti a quegli stessi veicoli
  perché condividono `related_sku_code = R304`.

---

## Regole da Seguire Quando si Creano Prodotti

### Prodotti NON universali (la maggioranza)
→ SEMPRE aggiungere `related_sku_code` come meta_data del prodotto.
→ Senza di esso il plugin non può collegare il prodotto ai veicoli compatibili.

### Prodotti universali (es. accessori, prodotti chimici)
→ `related_sku_code` non necessario o impostato a "universale".

### Come determinare il related_sku_code

1. Identifica la categoria del filtro (aria / olio a bagno / olio a vite / carburante a bagno / carburante a vite)
2. Usa il prefisso corretto: A / OP / R / N / RN
3. Il numero viene dal catalogo di riferimento (Tecnocar per filtri aria, o catalogo interno)

**Esempio workflow:**
```
Devo importare: Filtro Olio BMW N47 — marca Mann, codice W712/83
Categoria: filtro olio a vite → prefisso R
related_sku_code: R304 (se già esiste nel sistema) o nuovo codice Rxxx

Devo importare: stesso filtro BMW N47 — marca Mahle, codice OC 1044
related_sku_code: R304 (STESSO codice di Mann → sono cross-reference)
```

---

## Come Aggiungere related_sku_code al Prodotto

Il `related_sku_code` si salva come **meta_data WooCommerce**:

```json
{
  "name": "Filtro Olio Mann BMW N47",
  "sku": "MANN-W712-83",
  "regular_price": "12.50",
  "meta_data": [
    {"key": "related_sku_code", "value": "R304"}
  ]
}
```

Quando usi il tool `crea_prodotto` o `importa_prodotti_bulk`, passa il campo
`related_sku_code` e verrà salvato automaticamente come meta_data.

---

## Import CSV Compatibilità Veicoli

Il CSV di compatibilità usa `related_sku_code` come chiave:

```csv
related_sku_code,marca,modello,motorizzazione,anno_da,anno_a
R304,Fiat,Punto,1.3 Multijet,2003,2012
R304,Fiat,Panda,1.3 Multijet,2003,2012
R304,Lancia,Ypsilon,1.3 MJT,2004,2011
OP400,BMW,Serie 3,2.0d N47,2005,2012
A2181,Fiat,Punto,1.4,2003,2012
```

→ Tutti i prodotti con `related_sku_code=R304` vengono automaticamente
  collegati a Fiat Punto, Fiat Panda e Lancia Ypsilon.

---

## Checklist Creazione Prodotto Completa

Quando l'utente chiede di creare o importare prodotti ricambi:

- [ ] `nome` — chiaro e descrittivo con marca e compatibilità
- [ ] `sku` — codice univoco del prodotto (codice fornitore o interno)
- [ ] `prezzo` — prezzo di vendita calcolato con margine
- [ ] `descrizione` — include compatibilità veicoli
- [ ] `categoria` — categoria WooCommerce corretta
- [ ] `related_sku_code` — codice interno (R/OP/A/N/RN + numero) **OBBLIGATORIO per prodotti non universali**
- [ ] `attributi` — codice OE, marca auto, modello, anno, tipo motore
