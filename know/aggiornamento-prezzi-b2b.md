# Aggiornamento Prezzi B2B — Workflow Completo

## Panoramica

L'agente può controllare i prezzi sui portali B2B (AZ Car, Elring, altri) e aggiornare
i prezzi sul WooCommerce del negozio. Questo workflow è fondamentale per mantenere
margini corretti e prezzi competitivi.

---

## Logica di Pricing

### Formula Base
```
Prezzo vendita = Prezzo acquisto B2B × Ricarico
```

### Ricarichi Tipici Ricambi Auto
- **Filtri (olio, aria, abitacolo):** ricarico 2.0x – 2.5x
- **Pastiglie freno:** ricarico 1.8x – 2.2x
- **Dischi freno:** ricarico 1.6x – 2.0x
- **Kit distribuzione:** ricarico 1.5x – 1.8x
- **Ammortizzatori:** ricarico 1.7x – 2.0x
- **Componenti motore (guarnizioni, ecc.):** ricarico 1.5x – 2.0x
- **Parti carrozzeria:** ricarico 1.4x – 1.8x

**NOTA:** Chiedi sempre all'utente quale ricarico applicare. Non assumere.

### Prezzo di Listino vs Prezzo Reale
- I portali B2B mostrano spesso il prezzo di LISTINO (prezzo suggerito dal produttore)
- Il prezzo reale B2B è più basso per i rivenditori registrati
- Se hai accesso al portale B2B con login → il prezzo mostrato è quello reale
- Usa il prezzo reale B2B, non il listino, per calcolare il ricarico

---

## Workflow Aggiornamento Prezzi

### 1. Identifica Prodotti da Aggiornare
Opzioni:
- L'utente chiede di aggiornare un prodotto specifico
- Aggiornamento di massa di una categoria
- Controlla periodico di prodotti con margine basso

### 2. Trova il Prezzo B2B
Per trovare il prezzo di acquisto:
```
naviga_sito_con_istruzioni(
    url="https://www.azcar.it",
    istruzioni="Cerca il ricambio [codice/nome]. Trova il prezzo netto B2B."
)
```

Oppure leggi da CSV se già scaricato:
```
leggi_csv("prezzi_fornitore.csv")
```

### 3. Calcola il Nuovo Prezzo
```
nuovo_prezzo = prezzo_b2b × ricarico
```
Arrotonda in modo commerciale:
- Se > 10€ → arrotonda a x.90 o x.99
- Se < 10€ → arrotonda a x.99
- Esempio: 23.47 × 2.0 = 46.94 → 46.90

### 4. Aggiorna su WooCommerce

**Prodotto singolo:**
```
modifica_prodotto_completo(product_id=123, regular_price="46.90")
```

**Prodotti in massa:**
```
aggiorna_prezzi_bulk([
    {"product_id": 123, "regular_price": "46.90"},
    {"product_id": 124, "regular_price": "29.99"},
    ...
])
```

### 5. Registra le Modifiche
Salva nota per tracciabilità:
```
salva_nota("Prezzi aggiornati: [lista prodotti], fornitore: AZ Car, data: [oggi]")
```

---

## Gestione Sconti e Promozioni

### Sale Price
WooCommerce ha due campi prezzo:
- `regular_price` = prezzo pieno (quello che calcoli dal ricarico)
- `sale_price` = prezzo scontato (se vuoi fare una promozione)

Per impostare una promo:
```
modifica_prodotto_completo(
    product_id=123,
    regular_price="46.90",
    sale_price="39.90"
)
```

Per togliere la promo: imposta `sale_price=""` (stringa vuota)

---

## Portali B2B Principali

### AZ Car (azcar.it)
- Catalogo aftermarket ampio
- Cerca per codice ricambio o applicazione veicolo
- Prezzi netti visibili dopo login

### Elring (elring.de/it)
- Specializzato in guarnizioni motore
- Catalogo tecnico dettagliato
- Cross-reference con codici OEM

### Portali produttori (Mann, UFI, Brembo, ecc.)
- Ogni produttore ha il suo catalogo online
- Utili per dati tecnici più che per prezzi
- Cross-reference con codici OEM

---

## Controllo Margini

Quando aggiorni i prezzi, verifica:
1. Il margine è almeno il minimo stabilito dall'utente?
2. Il prezzo è competitivo rispetto ad Amazon/eBay?
3. Non stai vendendo sotto il prezzo minimo imposto dal produttore?

Segnala all'utente se:
- Un prodotto ha margine sotto il 30%
- Il prezzo B2B è aumentato significativamente
- Ci sono differenze anomale tra fornitori
