# AZ Car B2B — Importazione Prodotti con Cross-Reference

## Obiettivo

Accedere al portale AZ Car B2B, trovare i prodotti disponibili (verdi),
leggere il cross-reference per ogni prodotto, e creare i prodotti su WooCommerce
con il corretto `related_sku_code` e tutti i dati necessari.

---

## Step 1 — Accesso al Portale

Usa il tool `accedi_portale_b2b` con portale `azcar`.

Le credenziali sono già nel `.env` — non chiederle mai all'utente.

---

## Step 2 — Navigare il Catalogo

Nel portale AZ Car ogni prodotto ha un indicatore di disponibilità:

- 🟢 **Verde** = disponibile in magazzino → DA IMPORTARE
- 🔴 Rosso / grigio / altro = non disponibile → IGNORARE

**Regola fondamentale: importa SOLO i prodotti verdi (disponibili).**

---

## Step 3 — Leggere il Cross-Reference

Per ogni prodotto disponibile, clicca su **"Cross"** (o pulsante equivalente
di cross-reference nel portale).

Il cross mostra:
- Il codice del prodotto AZ Car (es. `UFI-23.438.00`)
- I codici equivalenti di altre marche (es. `MANN W712/83`, `MAHLE OC1044`, `JAPANPARTS FO-022JM`)
- Eventuali codici OE (originali casa costruttrice)

**Questi codici cross-reference sono fondamentali** — ogni codice equivalente
diventerà un prodotto separato su WooCommerce con lo stesso `related_sku_code`.

---

## Step 4 — Determinare il related_sku_code

Basandoti sul tipo di prodotto, assegna il `related_sku_code` usando i prefissi interni:

| Tipo prodotto | Prefisso | Esempi |
|---------------|----------|--------|
| Filtro Aria | `A` | A2181, A2183 (catalogo Tecnocar) |
| Filtro Olio a bagno (cartuccia) | `OP` | OP400, OP246 |
| Filtro Olio a vite (spin-on) | `R` | R304, R100 |
| Filtro Carburante a bagno | `N` | N311, N290 |
| Filtro Carburante a vite | `RN` | RN260, RN180 |

**Come trovare il codice corretto:**
- Guarda il codice AZ Car del prodotto
- Cerca se esiste già un `related_sku_code` nel sistema per quel prodotto
- Se non esiste, crea un nuovo codice con il prefisso corretto e il numero progressivo

**Esempio:**
```
Prodotto AZ Car: Filtro olio a vite per BMW N47
Codice AZ Car: UFI-23.438.00
Cross: MANN W712/83, MAHLE OC1044

→ related_sku_code: R304 (se già censito) oppure nuovo R-xxx
→ Tutti i prodotti in cross condividono lo stesso related_sku_code
```

---

## Step 5 — Creare i Prodotti su WooCommerce

Per ogni prodotto disponibile (verde), crea il prodotto con `crea_prodotto` o
usa `importa_prodotti_bulk` per importare in batch.

### Dati da estrarre da AZ Car per ogni prodotto:

```
nome:             "[Marca] [Tipo filtro] [Auto compatibile]"
sku:              codice AZ Car del prodotto (es. "UFI-23.438.00")
prezzo:           prezzo da AZ Car + margine configurato (default 30%)
descrizione:      tipo prodotto, marca, codice OE, compatibilità
categoria:        categoria WooCommerce corretta (es. "Filtri Olio")
related_sku_code: codice interno (R/OP/A/N/RN + numero)
attributi: {
  "codice_oe":  codice originale casa costruttrice
  "marca":      marca del ricambio (UFI, Mann, Mahle, ecc.)
  "tipo":       "a bagno" o "a vite" per i filtri olio
}
```

### Esempio prodotto completo:

```json
{
  "nome": "Filtro Olio UFI BMW Serie 3 2.0d N47",
  "sku": "UFI-23.438.00",
  "prezzo": 12.50,
  "descrizione": "Filtro olio a vite UFI per BMW Serie 3 E90 2.0d N47 (2005-2012). Codice OE: 11427566327.",
  "categoria": "Filtri Olio",
  "related_sku_code": "R304",
  "attributi": {
    "codice_oe": "11427566327",
    "marca": "UFI",
    "tipo": "a vite"
  }
}
```

---

## Step 6 — Gestire il Cross (più marche stesso prodotto)

Se il cross mostra più marche disponibili nel portale AZ Car, crea un prodotto
per **ogni marca disponibile e verde**, tutti con lo stesso `related_sku_code`.

```
R304 disponibile in:
✅ UFI 23.438.00 (verde)   → crea prodotto SKU "UFI-23.438.00", related: R304
✅ MANN W712/83 (verde)    → crea prodotto SKU "MANN-W712-83", related: R304
❌ MAHLE OC1044 (rosso)    → NON importare
✅ JAPANPARTS FO-022JM (verde) → crea prodotto SKU "JP-FO022JM", related: R304
```

→ 3 prodotti creati, stesso `related_sku_code`, prezzi diversi (costo AZ Car diverso per marca).

---

## Step 7 — Calcolo Prezzo

Usa il margine default dal `.env` (`MARGINE_PERCENTUALE`, default 30%) e
applica IVA (`ALIQUOTA_IVA`, default 22%).

Oppure usa il tool `calcola_prezzo_vendita` con il costo da AZ Car.

```
Costo AZ Car: €8.00
Margine 30%:  €10.40 (netto)
IVA 22%:      €12.69 (finale)
```

---

## Workflow Completo (Riepilogo)

```
1. accedi_portale_b2b("azcar", "naviga il catalogo [categoria]")
2. Per ogni prodotto VERDE (disponibile):
   a. Leggi nome, codice, prezzo
   b. Clicca "Cross" → leggi tutti i codici equivalenti
   c. Determina related_sku_code (prefisso + numero)
   d. Calcola prezzo con margine
   e. Crea prodotto su WooCommerce con related_sku_code
3. Per ogni marca nel cross che è VERDE:
   → crea prodotto separato, stesso related_sku_code
4. Prodotti ROSSI/non disponibili → ignora completamente
5. Salva in memoria: "Importati X prodotti categoria Y da AZ Car"
```

---

## Note Importanti

- **Non importare mai prodotti non verdi** — crea confusione nello stock
- **Il related_sku_code deve essere consistente** — se R304 esiste già,
  usa sempre R304 per quel filtro, non creare R304b o varianti
- **Ogni marca = SKU diverso** — non mescolare marche nello stesso prodotto
- **Se non sai il related_sku_code** di un prodotto, chiedi all'utente
  prima di procedere — meglio chiedere che sbagliare
