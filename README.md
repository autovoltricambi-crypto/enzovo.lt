# Agente AI Ricambi Auto

Assistente intelligente per ricerca ricambi auto sui cataloghi B2B, confronto prezzi, export CSV e memoria persistente.

## Funzionalità

- **Ricerca cataloghi B2B** — Cerca prodotti su Elring, Corteco, Valeo e AutoDoc
- **Confronto prezzi** — Confronta prezzi dello stesso ricambio tra fornitori
- **Export CSV** — Esporta i risultati in CSV (separatore `;` per Excel italiano)
- **Calcolo prezzi** — Margine (default 30%) + IVA (22%) automatici
- **Navigazione web** — Apre e legge qualsiasi pagina web
- **Memoria** — Ricorda ogni ricerca e prodotto. Non cerca due volte la stessa cosa.
- **Esperto ricambi** — Conosce codici OE, cross-reference, alternative aftermarket

## Installazione rapida

```bash
# 1. Entra nella cartella
cd agente-ricambi

# 2. Crea ambiente virtuale
python -m venv venv
source venv/bin/activate        # Mac/Linux
# venv\Scripts\activate         # Windows

# 3. Installa dipendenze
pip install -r requirements.txt

# 4. Configura API key
cp .env.example .env
# Apri .env e inserisci la tua ANTHROPIC_API_KEY

# 5. Avvia
python app.py
```

Poi apri il browser su **http://127.0.0.1:8000**

## Come usarlo

### Ricerca prodotti
- "Cerca guarnizione testata BMW N47 su Elring"
- "Cerca paraolio albero motore Fiat 1.3 MJT su tutti i cataloghi"
- "Cerca il codice OE 11427566327 su AutoDoc"

### Confronto prezzi
- "Confronta i prezzi del kit frizione Valeo per Fiat Punto tra Valeo e AutoDoc"

### Export CSV
- "Esporta in CSV tutti i risultati che hai trovato"
- "Crea un CSV con i prodotti Corteco per BMW Serie 3"

### Calcolo prezzi
- "Calcola il prezzo di vendita per un pezzo da 45€"
- "Applica margine 25% e IVA al costo fornitore di 120€"

### Memoria
- "Cosa hai in memoria?"
- "Hai già cercato filtri olio BMW?"
- "Salva una nota: Corteco ha tempi di consegna 3-5 giorni"

## Struttura progetto

```
agente-ricambi/
├── app.py                 # Server web FastAPI
├── agent_simple.py        # Logica agente + tool definitions
├── config.py              # Configurazione
├── requirements.txt       # Dipendenze
├── .env.example           # Template variabili ambiente
├── static/
│   └── index.html         # Interfaccia chat
├── tools/
│   ├── cataloghi.py       # Scraping cataloghi B2B + login WordPress
│   ├── csv_export.py      # Generazione CSV
│   ├── memoria.py         # Memoria persistente JSON
│   ├── prezzi.py          # Calcolo margini e IVA
│   └── wordpress_write.py # API WooCommerce/WordPress
├── data/
│   └── memoria.json       # File memoria (auto-generato)
└── exports/               # CSV esportati (auto-generato)
```

## Cataloghi supportati

| Catalogo | Specializzazione |
|----------|-----------------|
| **Elring** | Guarnizioni, tenute, bulloneria motore |
| **Corteco** | Paraolio, supporti motore/cambio, sospensioni |
| **Valeo** | Frizioni, alternatori, motorini, illuminazione |
| **AutoDoc** | Multi-marca, ricambi generici, prezzi competitivi |

## Note tecniche

- La memoria è in `data/memoria.json` — puoi copiarla/backupparla
- I CSV esportati vanno in `exports/` — scaricabili anche dal browser
- Il separatore CSV è `;` per compatibilità con Excel italiano
- L'agente usa Claude Sonnet 4.6 via API Anthropic
- Ogni ricerca sui cataloghi viene auto-salvata in memoria

## Debug navigazione browser-use

Se il tool `naviga_web` esegue la navigazione correttamente nel browser ma la chat
riporta un errore di "pagina non caricata", segui questi passi:

### 1. Rendi il browser visibile

Nel file `.env` imposta:

```env
BROWSER_HEADLESS=false
```

Così vedi esattamente cosa fa il browser durante la navigazione.

### 2. Usa il tuo profilo Chrome (opzionale, riduce captcha)

```env
# Mac
CHROME_USER_DATA_DIR=/Users/TUO_NOME/Library/Application Support/Google/Chrome
# Windows
# CHROME_USER_DATA_DIR=C:\Users\TUO_NOME\AppData\Local\Google\Chrome\User Data
# Linux
# CHROME_USER_DATA_DIR=/home/TUO_NOME/.config/google-chrome
CHROME_PROFILE=Default
```

### 3. Reinstalla Playwright se Chromium non parte

```bash
pip install -r requirements.txt
python -m playwright install chromium
```

### 4. Riavvia il server

```bash
uvicorn app:app --reload
```

### 5. Verifica con l'endpoint health-check

Apri il browser su:

```
http://127.0.0.1:8000/api/debug/browser
```

Ritorna un JSON con:
- `versioni` — pacchetti installati (`browser_use`, `playwright`, ecc.)
- `test` — risultato del test di navigazione su `example.com`
- `errore` — stack trace completo se qualcosa non va

### Come funzionano i due agenti

Il sistema usa **due modelli separati**:

| Modello | Ruolo |
|---------|-------|
| **Claude Haiku** | Agente chat principale — interpreta i messaggi e chiama i tool |
| **Claude Sonnet** | Agente browser-use — naviga il web dentro Chromium |

I due agenti comunicano tramite il risultato del tool (`naviga_web`, `accedi_portale_b2b`, ecc.):
il risultato JSON viene passato a Claude Haiku che lo interpreta e risponde in chat.
Se `agent.run()` lancia un'eccezione dopo aver navigato con successo
(es. errore di cleanup, timeout sul risultato finale), il tool ora restituisce
comunque `successo: true` con i dati parziali, evitando falsi errori in chat.
