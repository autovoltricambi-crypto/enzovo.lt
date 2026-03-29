# Debug Frontend, WordPress, Fetch e DOM

## Obiettivo

Dare all'agente una procedura pratica per diagnosticare problemi su frontend statici,
interfacce WordPress e chiamate `fetch` senza andare a tentoni.

---

## Workflow di Debug

Quando qualcosa "non funziona", separa sempre il problema in 4 livelli:

1. **Browser/UI**
   - il bottone si vede?
   - il layout è corretto?
   - l'elemento è cliccabile?

2. **DOM/JavaScript**
   - il selettore trova davvero l'elemento?
   - l'evento viene agganciato?
   - c'è un errore in console?

3. **Network / fetch**
   - la richiesta parte?
   - ritorna 200, 401, 404, 500?
   - il payload JSON è quello atteso?

4. **Backend / WordPress**
   - l'endpoint esiste?
   - l'autenticazione è valida?
   - la risorsa WordPress è un post, una pagina, una categoria o un template?

Non mischiare i livelli: prima trova dove si rompe davvero il flusso.

---

## Debug Frontend

### Errori frequenti

#### 1. `Cannot read properties of null`
Significa che il selettore non ha trovato l'elemento.

Cause tipiche:
- ID o classe sbagliati
- script eseguito prima che il DOM sia pronto
- elemento creato dinamicamente ma letto troppo presto

Check:

```js
const el = document.getElementById('send-btn');
console.log(el);
```

Se `null`, il problema non è nel click ma nel selettore o nel timing.

#### 2. Evento non parte

```js
button.addEventListener('click', () => {
  console.log('click');
});
```

Se il log non appare:
- il listener non è stato agganciato
- l'elemento è coperto da un overlay
- il bottone è `disabled`

#### 3. UI aggiornata ma poi sparisce

Spesso succede quando:
- fai `innerHTML = ...` su un contenitore che sostituisce nodi con listener già agganciati
- un render successivo sovrascrive il contenuto

---

## Debug Fetch

### Checklist base

```js
const res = await fetch('/api/sessioni');
console.log(res.status, res.ok);
const data = await res.json();
console.log(data);
```

### Problemi tipici

#### `TypeError: Failed to fetch`
Possibili cause:
- server non attivo
- URL errata
- CORS bloccato
- HTTPS/HTTP misti

#### 404
- endpoint sbagliato
- route non registrata

#### 401 / 403
- autenticazione mancante
- credenziali WordPress errate
- permessi insufficienti

#### 500
- errore backend
- payload non previsto
- eccezione Python/PHP lato server

### Regola

Su `fetch`, controlla sempre:
- URL chiamata
- status code
- contenuto JSON reale
- eventuale differenza tra quello che il frontend si aspetta e quello che il backend restituisce

---

## Debug DOM

### Selettori robusti

```js
const panel = document.getElementById('panel-sessioni');
if (!panel) {
  console.error('panel-sessioni non trovato');
}
```

### Elementi nascosti

Se un elemento "esiste ma non si vede":
- controlla `display: none`
- controlla `visibility: hidden`
- controlla `overflow: hidden` nel genitore
- controlla se è fuori viewport per colpa del layout

### Render condizionale

Molti bug DOM non sono bug di JavaScript puro ma bug di stato:
- la funzione render non viene chiamata
- viene chiamata con array vuoto
- il tab/pannello corretto non viene attivato

---

## Debug WordPress

### Distinzione critica

- **Pagina (`page`)**: contenuto statico tipo Chi siamo, Contatti, Landing page
- **Post (`post`)**: articolo blog
- **Categoria blog**: tassonomia dei post
- **Categoria prodotto WooCommerce**: tassonomia diversa, non è la stessa cosa del blog

Se l'utente dice:
"crea la pagina dove vanno gli articoli del blog"

non assumere subito che basti una pagina HTML.
Potrebbe voler dire:
- creare una pagina introduttiva blog,
- impostare/gestire la pagina archivio articoli,
- creare categorie blog,
- pubblicare i post dentro quelle categorie.

### Categorie blog

Le categorie blog devono essere:
- poche e stabili
- coerenti nel tempo
- riusate dai post futuri

Esempi sensati per un sito come auto-volt.it:
- Manutenzione Auto
- Guide Ricambi
- Problemi e Diagnosi
- News Auto Elettriche
- Consigli Acquisto Ricambi

### Regola operativa

Se stai impostando il blog:
1. definisci prima le categorie
2. crea o verifica l'architettura del blog
3. solo dopo crea i post
4. assegna sempre ogni post alla categoria più adatta

---

## Debug WordPress REST API

### Controlli rapidi

- l'endpoint `/wp-json/wp/v2/...` risponde?
- il client è autenticato?
- stai usando `posts`, `pages`, `categories` o endpoint WooCommerce corretti?

### Errori comuni

- creare un post pensando di aver creato una pagina
- creare una categoria prodotto pensando sia una categoria blog
- aspettarsi che una pagina HTML diventi automaticamente archivio post
- confondere categorie blog con menu di navigazione o template del tema

---

## Pattern di Debug Consigliato

Per bug frontend/WordPress:

1. leggi il problema letterale dell'utente
2. identifica il livello che si rompe: UI, DOM, fetch, backend, WordPress
3. raccogli una prova concreta
4. correggi la causa radice
5. verifica che il flusso completo funzioni davvero

---

## Quando consultare questo file

Leggere questo file se il task riguarda:
- errori `fetch`
- problemi DOM o event listener
- pannelli/tab che non si vedono
- WordPress REST API
- differenza tra post, pagine e categorie blog
- struttura di un blog WordPress