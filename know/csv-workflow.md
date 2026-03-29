# Workflow CSV — Guida Operativa

## Struttura CSV Compatibilità Veicoli (quello dell'utente)

Il CSV che l'utente usa per il plugin compatibilità ha queste colonne:
- **related_sku_code** — codice interno che raggruppa prodotti identici di marche diverse (es: R304)
- **marca** — marca veicolo (es: Fiat, BMW, Volkswagen)
- **modello** — modello veicolo (es: Panda, Serie 3, Golf)
- **motore** — motorizzazione (es: 1.2 60cv, 2.0d 150cv N47)

**Questo CSV NON contiene OEM, prezzi, descrizioni o SKU.**
Serve SOLO per il collegamento prodotti ↔ veicoli nel plugin.

---

## Come Lavorare sui CSV

### Quando l'utente ti manda un CSV
1. Leggilo con `leggi_csv(nome_file)` per capire struttura e contenuto
2. Identifica il `related_sku_code` e i veicoli associati
3. Se chiede di modificare descrizioni → usa `modifica_csv` o `modifica_csv_bulk`
4. Se chiede di aggiungere colonne (es: OEM) → usa `aggiungi_colonna_csv` poi `modifica_csv`

### Creare un CSV OEM separato
Quando devi raccogliere codici OEM per un `related_sku_code`:
1. Cerca su portali B2B o web il codice OE originale per quel ricambio
2. Cerca i cross-reference (codici aftermarket equivalenti)
3. Crea un nuovo CSV con `esporta_csv` contenente: related_sku_code, oem, marca_ricambio, codice_ricambio
4. Questo CSV è tuo — lo usi per aggiornare le descrizioni su WooCommerce

### Aggiornare prodotti WooCommerce dopo aver lavorato sul CSV
1. `cerca_prodotti_per_related_sku("R304")` → trovi tutti i prodotti con quel codice
2. Per ogni prodotto, aggiorna la descrizione includendo gli OEM trovati
3. Usa `aggiorna_descrizioni_bulk` per aggiornarli tutti in un colpo

---

## Regole Importanti

- **NON modificare il related_sku_code** nel CSV dell'utente a meno che non lo chieda esplicitamente
- **I CSV vanno in exports/** — sia quelli dell'utente che quelli che crei tu
- **Separatore `;`** per Excel italiano (il tool lo gestisce automaticamente)
- **Encoding UTF-8-sig** (con BOM) per caratteri italiani in Excel
- Quando crei OEM, metti sempre il codice OE originale come primo riferimento
- Se un prodotto ha più codici OEM, separali con virgola nella stessa cella
