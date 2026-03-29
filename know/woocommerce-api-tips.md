# WooCommerce REST API — Tips e Gotchas per l'Agente

## Concetti Chiave

### Identificare Prodotti
- **product_id**: ID numerico univoco, assegnato da WordPress. Immutabile.
- **SKU**: codice articolo impostato dall'utente. Può essere vuoto.
- **related_sku_code**: meta_data personalizzato che collega il prodotto ai veicoli compatibili. 
  **Questo è il campo principale per cercare prodotti per compatibilità auto.**

### Cercare Prodotti

Per cercare prodotti per compatibilità veicolo:
```
cerca_prodotti_per_related_sku("codice-related-sku")
```

Per cercare prodotti per nome/testo:
```
cerca_prodotti(query="filtro olio mann")
```

Per cercare per SKU esatto:
```
cerca_prodotti(query="", sku="W712/73")
```

**ATTENZIONE:** L'API WooCommerce cerca per `search` nel nome del prodotto, non nella descrizione.
Per cercare nella descrizione o nei meta_data, servono filtri custom o ricerca manuale.

---

## Aggiornamento Prodotti

### Modifica Prodotto Singolo
```
modifica_prodotto_completo(
    product_id=123,
    name="Nuovo nome",
    regular_price="29.90",
    description="<p>Descrizione lunga HTML</p>",
    short_description="<p>Breve descrizione</p>"
)
```

### Aggiornamento Descrizioni in Massa
```
aggiorna_descrizioni_bulk([
    {"product_id": 123, "description": "<p>Nuova descrizione</p>"},
    {"product_id": 124, "description": "<p>Altra descrizione</p>"},
    ...
])
```
→ Usa l'API batch: `POST /wp-json/wc/v3/products/batch` con `update: [...]`
→ Max 100 prodotti per batch (limite WooCommerce)

### Aggiornamento Prezzi in Massa
```
aggiorna_prezzi_bulk([
    {"product_id": 123, "regular_price": "29.90", "sale_price": "24.90"},
    ...
])
```

---

## meta_data

I meta_data sono campi personalizzati dei prodotti WooCommerce.
Struttura in API:
```json
{
    "meta_data": [
        {"key": "related_sku_code", "value": "ABC123"},
        {"key": "_altro_campo", "value": "valore"}
    ]
}
```

### Per aggiornare meta_data:
```
modifica_prodotto_completo(
    product_id=123,
    meta_data=[{"key": "related_sku_code", "value": "NUOVOCOD"}]
)
```

**ATTENZIONE:** Inviare meta_data in update NON cancella gli altri meta. Aggiorna/aggiunge solo quelli specificati.

---

## Immagini Prodotto

### Aggiungere immagine da URL
```
modifica_prodotto_completo(
    product_id=123,
    images=[{"src": "https://esempio.com/foto.jpg"}]
)
```

**ATTENZIONE:** Inviare images in update SOSTITUISCE tutte le immagini. Se vuoi aggiungere senza perdere le vecchie:
1. Prima leggi le immagini attuali del prodotto
2. Aggiungi la nuova alla lista esistente
3. Invia la lista completa

---

## Categorie e Tag

### Assegnare categorie
I prodotti possono avere più categorie:
```
modifica_prodotto_completo(
    product_id=123,
    categories=[{"id": 15}, {"id": 22}]
)
```

### Attenzione con le Categorie
- Servono gli ID numerici delle categorie, non i nomi
- Per ottenere gli ID: `GET /wp-json/wc/v3/products/categories?search=filtri`
- Le categorie sono gerarchiche (parent → child)

---

## Limiti API

### Rate Limiting
- WooCommerce di default non ha rate limiting stretto
- Ma il server potrebbe avere limiti (es. Cloudflare, hosting)
- Non inviare più di 10 batch request in rapida successione
- Aggiungi piccole pause tra batch grandi

### Batch API Limits
- Max 100 operazioni per batch request
- Per grandi volumi, spezzare in batch da 50-100
- La batch API restituisce risultati per ogni operazione

### Paginazione
- Per default, l'API restituisce max 100 risultati per pagina
- Usa `per_page=100` e `page=N` per paginare
- Controlla header `X-WP-Total` per il totale risultati

---

## Errori Comuni

### 404 Not Found
- Prodotto/post non esiste con quell'ID
- Verifica che l'ID sia corretto

### 400 Bad Request
- Formato dati errato
- Prezzo deve essere stringa: `"29.90"` non `29.90`
- Meta_data deve essere lista di dict con key e value

### 401 Unauthorized
- Consumer key/secret errati o scaduti
- Verifica in config.py

### Timeout
- Upload immagini grandi può essere lento
- Batch con 100 prodotti può richiedere 30+ secondi
- Il tool ha timeout di 60 secondi — per batch grandi, spezzare in gruppi più piccoli

---

## WordPress REST API (Blog)

### Creare Post
```
crea_post_blog(
    titolo="Titolo articolo",
    contenuto_html="<h2>Sezione</h2><p>Testo</p>",
    slug="url-articolo",
    stato="draft",          # oppure "publish"
    categoria="Guide Ricambi",
    tags=["fiat", "filtro-olio"],
    excerpt="Meta description per SEO"
)
```

### Stato dei Post
- `draft` = bozza, non visibile sul sito
- `publish` = pubblicato e visibile
- `private` = visibile solo agli admin
- **REGOLA:** Crea sempre in `draft` e chiedi conferma prima di pubblicare

### Categorie Blog vs Categorie Prodotto
- Le categorie blog (WordPress) e le categorie prodotto (WooCommerce) sono SEPARATE
- Non confonderle: hanno endpoint diversi e ID diversi
