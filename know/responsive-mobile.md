# Responsive Mobile — Basi Operative

## Obiettivo

Costruire interfacce che funzionino bene su cellulare prima ancora che su desktop.
L'agente deve ragionare in ottica mobile-first.

---

## Regola Base

Partire da layout mobile e poi aggiungere adattamenti per schermi più larghi.

```css
.container {
  width: 100%;
  padding: 0 16px;
}

@media (min-width: 768px) {
  .container {
    max-width: 720px;
    margin: 0 auto;
  }
}
```

---

## Viewport

Ogni pagina deve avere:

```html
<meta name="viewport" content="width=device-width, initial-scale=1.0">
```

Senza questo tag, la pagina su smartphone non scala correttamente.

---

## Layout Mobile-First

### Stack verticale su mobile

```css
.toolbar {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

@media (min-width: 768px) {
  .toolbar {
    flex-direction: row;
    align-items: center;
  }
}
```

### Grid adattiva

```css
.cards {
  display: grid;
  grid-template-columns: 1fr;
  gap: 12px;
}

@media (min-width: 768px) {
  .cards {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (min-width: 1024px) {
  .cards {
    grid-template-columns: repeat(3, 1fr);
  }
}
```

---

## Regole Pratiche per Mobile

- Evitare larghezze fisse tipo `width: 400px`
- Usare `max-width: 100%` su immagini e contenitori
- Ridurre padding e gap su schermi stretti
- Permettere il wrap di pulsanti e badge
- Evitare header troppo alti o toolbar con troppi controlli in una sola riga

### Immagini responsive

```css
img {
  max-width: 100%;
  height: auto;
  display: block;
}
```

---

## Tipografia Mobile

### Regole base

- testo base: `14px`-`16px`
- line-height: `1.4`-`1.6`
- evitare testi troppo piccoli sotto `13px`
- limitare righe troppo lunghe

```css
body {
  font-size: 16px;
  line-height: 1.5;
}

.meta {
  font-size: 0.78rem;
}
```

---

## Pulsanti e Touch Target

Su cellulare i clic devono essere facili.

- altezza minima consigliata: `40px`-`44px`
- spazio tra pulsanti vicini
- aree cliccabili non troppo piccole

```css
.btn {
  min-height: 44px;
  padding: 10px 14px;
}
```

---

## Overflow e Contenuti Lunghi

Per evitare layout rotti:

```css
.card {
  min-width: 0;
}

.text {
  word-break: break-word;
}
```

### Tabelle grandi

Se una tabella non entra su mobile:
- metterla in un contenitore con `overflow-x: auto`
- oppure trasformarla in card list se il contenuto è semplice

```css
.table-wrap {
  overflow-x: auto;
}
```

---

## Pattern UI Utili

### Sidebar su mobile

- su desktop può stare fissa
- su mobile va spostata sotto il contenuto o trasformata in drawer

### Tabs

- usare tab corte
- permettere wrap o scroll orizzontale se sono molte

### Modali

- su mobile usare larghezza quasi piena
- altezza massima con scroll interno

---

## Breakpoint Pratici

- base mobile: nessuna media query
- tablet: `@media (min-width: 768px)`
- desktop: `@media (min-width: 1024px)`

Non servono troppi breakpoint se il layout è semplice.

---

## Checklist Responsive

Prima di considerare finita una UI, verificare:

- testo leggibile senza zoom
- pulsanti facili da premere
- nessun overflow orizzontale indesiderato
- header e toolbar non collassano male
- card e pannelli vanno uno sotto l'altro su mobile
- immagini e iframe non escono dal contenitore
- textarea/input restano usabili con tastiera mobile

---

## Quando l'agente deve consultare questo file

Leggere questo file se il task riguarda:
- adattare pagine per smartphone
- correggere layout rotti su schermi piccoli
- migliorare header, tab, card, form o modali per mobile
- progettare CSS responsive mobile-first