# HTML e CSS — Nozioni di Base

## Struttura HTML

```html
<!DOCTYPE html>
<html lang="it">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Titolo Pagina</title>
  <link rel="stylesheet" href="style.css">
</head>
<body>
  <!-- contenuto -->
</body>
</html>
```

---

## Tag Principali

### Struttura
| Tag | Uso |
|-----|-----|
| `<header>` | Intestazione pagina o sezione |
| `<nav>` | Menu di navigazione |
| `<main>` | Contenuto principale |
| `<section>` | Sezione tematica |
| `<article>` | Contenuto autonomo (prodotto, post) |
| `<aside>` | Barra laterale |
| `<footer>` | Piè di pagina |
| `<div>` | Contenitore generico (blocco) |
| `<span>` | Contenitore generico (inline) |

### Testo
| Tag | Uso |
|-----|-----|
| `<h1>` … `<h6>` | Titoli (h1 = principale, uno per pagina) |
| `<p>` | Paragrafo |
| `<strong>` | Testo in grassetto (semantico) |
| `<em>` | Testo in corsivo (semantico) |
| `<ul>` / `<ol>` | Lista non ordinata / ordinata |
| `<li>` | Elemento lista |
| `<a href="...">` | Link |
| `<br>` | Interruzione di riga |

### Media
| Tag | Uso |
|-----|-----|
| `<img src="..." alt="...">` | Immagine |
| `<picture>` | Immagine responsiva con sorgenti multiple |
| `<video>` | Video |

### Form
| Tag | Uso |
|-----|-----|
| `<form>` | Modulo |
| `<input type="text">` | Campo testo |
| `<input type="email">` | Campo email |
| `<input type="submit">` | Pulsante invio |
| `<select>` / `<option>` | Menu a tendina |
| `<textarea>` | Area di testo |
| `<label>` | Etichetta campo |
| `<button>` | Pulsante generico |

---

## CSS — Selettori

```css
/* Tag */
p { color: red; }

/* Classe */
.nome-classe { color: blue; }

/* ID */
#nome-id { color: green; }

/* Discendente */
.card p { font-size: 14px; }

/* Pseudo-classe */
a:hover { text-decoration: underline; }
li:first-child { font-weight: bold; }

/* Pseudo-elemento */
p::first-line { font-variant: small-caps; }
```

---

## CSS — Box Model

Ogni elemento è una scatola:

```
┌─────────────────────────────┐
│           margin            │
│  ┌───────────────────────┐  │
│  │        border         │  │
│  │  ┌─────────────────┐  │  │
│  │  │     padding     │  │  │
│  │  │  ┌───────────┐  │  │  │
│  │  │  │  content  │  │  │  │
│  │  │  └───────────┘  │  │  │
│  │  └─────────────────┘  │  │
│  └───────────────────────┘  │
└─────────────────────────────┘
```

```css
.box {
  width: 300px;
  padding: 16px;          /* spazio interno */
  border: 1px solid #ccc; /* bordo */
  margin: 24px auto;      /* spazio esterno, centrato */
  box-sizing: border-box; /* padding incluso nella width */
}
```

---

## CSS — Unità di Misura

| Unità | Descrizione | Uso tipico |
|-------|-------------|------------|
| `px` | Pixel fissi | Bordi, icone |
| `%` | Percentuale del contenitore | Larghezze fluide |
| `em` | Relativa al font del genitore | Padding, margin |
| `rem` | Relativa al font root (html) | Testi, spaziature |
| `vw` | % larghezza viewport | Layout full-width |
| `vh` | % altezza viewport | Hero section, modal |
| `fr` | Frazione (solo CSS Grid) | Colonne grid |

---

## CSS Responsive — Media Query

Breakpoint standard (mobile-first):

```css
/* Base: mobile (<768px) — nessuna media query */
.container {
  width: 100%;
  padding: 0 16px;
}

/* Tablet (768px+) */
@media (min-width: 768px) {
  .container {
    max-width: 720px;
    margin: 0 auto;
  }
}

/* Desktop (1024px+) */
@media (min-width: 1024px) {
  .container {
    max-width: 1200px;
  }
}
```

---

## CSS Flexbox

Allinea elementi su una riga o colonna.

```css
.flex-container {
  display: flex;
  flex-direction: row;        /* row | column */
  justify-content: center;    /* allineamento asse principale */
  align-items: center;        /* allineamento asse secondario */
  gap: 16px;                  /* spazio tra gli elementi */
  flex-wrap: wrap;            /* va a capo se non c'è spazio */
}

.flex-item {
  flex: 1;                    /* cresce per riempire lo spazio */
}
```

**Valori `justify-content`:**
- `flex-start` — allineati a sinistra
- `flex-end` — allineati a destra
- `center` — centrati
- `space-between` — spazio tra gli elementi
- `space-around` — spazio attorno agli elementi

---

## CSS Grid

Layout a griglia bidimensionale.

```css
.grid-container {
  display: grid;
  grid-template-columns: repeat(3, 1fr); /* 3 colonne uguali */
  gap: 24px;
}

/* Responsivo: 1 colonna su mobile, 3 su desktop */
.grid-container {
  display: grid;
  grid-template-columns: 1fr;
  gap: 16px;
}

@media (min-width: 768px) {
  .grid-container {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (min-width: 1024px) {
  .grid-container {
    grid-template-columns: repeat(3, 1fr);
  }
}
```

---

## Immagini Responsive

```html
<!-- Immagine che non supera il contenitore -->
<img src="foto.jpg" alt="descrizione" style="max-width: 100%; height: auto;">

<!-- Immagine con formato moderno (WebP + fallback) -->
<picture>
  <source srcset="foto.webp" type="image/webp">
  <img src="foto.jpg" alt="descrizione">
</picture>
```

```css
img {
  max-width: 100%;
  height: auto;
  display: block;
}
```

---

## Tipografia Responsive

```css
/* Fluid typography con clamp */
h1 {
  font-size: clamp(1.5rem, 4vw, 3rem);
  /* min: 1.5rem, preferito: 4% della viewport, max: 3rem */
}

p {
  font-size: 1rem;       /* 16px di default */
  line-height: 1.6;      /* interlinea leggibile */
  max-width: 65ch;       /* max 65 caratteri per riga — leggibilità */
}
```

---

## Pattern Responsivi Comuni

### Card griglia prodotti
```css
.prodotti-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 24px;
}
```
`auto-fill` + `minmax` crea automaticamente quante colonne entrano — nessuna media query necessaria.

### Navbar mobile/desktop
```css
/* Mobile: hamburger */
.nav-links { display: none; }
.nav-links.aperto { display: flex; flex-direction: column; }

/* Desktop: riga */
@media (min-width: 768px) {
  .nav-links { display: flex; flex-direction: row; gap: 24px; }
  .hamburger { display: none; }
}
```

### Centrare un elemento
```css
/* Flexbox */
.parent {
  display: flex;
  justify-content: center;
  align-items: center;
}

/* Margin auto (blocco con larghezza definita) */
.box {
  width: 600px;
  margin: 0 auto;
}
```

---

## Reset CSS di Base

```css
*, *::before, *::after {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

html {
  font-size: 16px;
}

body {
  font-family: system-ui, sans-serif;
  line-height: 1.5;
  color: #333;
}

img, video {
  max-width: 100%;
  display: block;
}
```

---

## Checklist Pagina Responsive

- [ ] `<meta name="viewport" content="width=device-width, initial-scale=1.0">` presente
- [ ] `box-sizing: border-box` su tutti gli elementi
- [ ] Nessuna larghezza fissa in pixel su contenitori principali
- [ ] Immagini con `max-width: 100%`
- [ ] Font leggibili su mobile (min 16px)
- [ ] Bottoni/link toccabili (min 44×44px)
- [ ] Testato su 320px (mobile piccolo), 768px (tablet), 1280px (desktop)
