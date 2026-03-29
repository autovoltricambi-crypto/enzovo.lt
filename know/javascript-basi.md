# JavaScript — Basi Operative

## Obiettivo

Fornire all'agente le basi pratiche per leggere, scrivere e modificare JavaScript semplice
in pagine HTML, interfacce admin e piccoli tool frontend.

---

## Concetti Base

### Variabili

```js
const apiUrl = '/api/sessioni';
let counter = 0;
let isLoading = false;
```

- `const` per valori che non devono essere riassegnati
- `let` per valori che cambiano
- Evitare `var`

### Tipi principali

- string: `"ciao"`
- number: `42`
- boolean: `true`, `false`
- array: `[1, 2, 3]`
- object: `{ nome: "Mario", ruolo: "admin" }`
- null: valore intenzionalmente vuoto
- undefined: valore non ancora definito

---

## Funzioni

### Funzione classica

```js
function somma(a, b) {
  return a + b;
}
```

### Arrow function

```js
const formatPrice = (value) => {
  return Number(value).toFixed(2);
};
```

Usare arrow function per callback e funzioni brevi.

---

## Condizioni e cicli

```js
if (isLoading) {
  console.log('Caricamento...');
} else {
  console.log('Pronto');
}

for (const item of items) {
  console.log(item.nome);
}

const filtrati = items.filter((item) => item.attivo);
const nomi = items.map((item) => item.nome);
```

Preferire `for...of`, `map`, `filter`, `find` rispetto a loop più verbosi quando basta.

---

## DOM — Selezionare e Modificare Elementi

```js
const button = document.getElementById('send-btn');
const cards = document.querySelectorAll('.sess-card');
```

### Modificare contenuto

```js
title.textContent = 'Nuovo titolo';
container.innerHTML = '<strong>Attenzione</strong>';
```

- `textContent` è più sicuro per testo semplice
- `innerHTML` solo se serve inserire markup HTML

### Classi CSS

```js
panel.classList.add('visible');
panel.classList.remove('visible');
panel.classList.toggle('visible', isOpen);
```

### Attributi

```js
image.setAttribute('alt', 'Filtro olio BMW');
link.href = '/api/download/file.csv';
```

---

## Eventi

```js
sendBtn.addEventListener('click', invia);

msgInput.addEventListener('keydown', (e) => {
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault();
    invia();
  }
});
```

Regole pratiche:
- usare `addEventListener`
- evitare handler inline complessi
- chiamare `preventDefault()` quando serve bloccare il comportamento standard

---

## Async / Await e Fetch

```js
async function caricaSessioni() {
  const res = await fetch('/api/sessioni');
  const data = await res.json();
  return data;
}
```

### Gestione errori

```js
async function caricaDati() {
  try {
    const res = await fetch('/api/memoria');
    if (!res.ok) throw new Error('Risposta non valida');
    return await res.json();
  } catch (err) {
    console.error('Errore caricamento', err);
    return null;
  }
}
```

Linee guida:
- controllare `res.ok` per richieste HTTP importanti
- usare `try/catch` su chiamate async esterne
- mostrare all'utente uno stato di errore leggibile

---

## Render di Liste

```js
function renderItems(items) {
  list.innerHTML = items.map((item) => {
    return `<div class="card">${escHtml(item.nome)}</div>`;
  }).join('');
}
```

### Escape HTML

Quando inserisci contenuti dinamici in `innerHTML`, sanitizza almeno i caratteri base:

```js
function escHtml(text) {
  return String(text)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;');
}
```

---

## Stato UI

Pattern semplice utile per interfacce admin:

```js
let isLoading = false;

function setLoading(value) {
  isLoading = value;
  sendBtn.disabled = value;
  spinner.hidden = !value;
}
```

Se l'interfaccia ha loading, errore e contenuto:
- definire funzioni chiare per aggiornare lo stato
- non mischiare fetch, trasformazione dati e render nello stesso blocco troppo lungo

---

## Best Practice

- Preferire funzioni piccole e nominate bene
- Separare `fetch`, `render`, `eventi`
- Usare `textContent` quando non serve HTML
- Evitare codice duplicato nei render
- Tenere i selettori DOM in alto se riutilizzati molte volte
- Non usare librerie se basta JavaScript nativo

---

## Quando l'agente deve consultare questo file

Leggere questo file se il task riguarda:
- pulsanti, click, input, eventi tastiera
- fetch API e chiamate al backend
- rendering di liste/cards/tabelle
- errori JavaScript semplici
- interazioni DOM in HTML statico