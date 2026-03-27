# SEO per E-commerce

## Sfide Specifiche dell'E-commerce

1. **Migliaia di pagine prodotto** da ottimizzare
2. **Duplicate content** da descrizioni fornitore
3. **Pagine filtro/sorting** che generano URL duplicate
4. **Prodotti esauriti** — cosa fare con le pagine?
5. **Stagionalità** dell'inventario

## Architettura dell'E-commerce

### Struttura URL Ottimale
```
/[categoria]/[sottocategoria]/[prodotto]/

Esempi:
/filtri/filtri-olio/filtro-olio-bmw-serie3-n47-elring/
/freni/pastiglie/pastiglie-bosch-fiat-punto-anteriori/
/sospensioni/ammortizzatori/ammortizzatore-bilstein-vw-golf-anteriore/
```

### Pagine Categoria — Il Vero Asset SEO
Le pagine categoria rankano per keyword competitive (volume alto).

**Ottimizzazione categoria:**
- H1: "Filtri Olio BMW — Prezzi e Offerte Online"
- Testo descrittivo sopra i prodotti (200-300 parole)
- Testo aggiuntivo in fondo alla pagina (SEO senza disturbare UX)
- Breadcrumb strutturato
- Link interni alle sottocategorie
- Schema BreadcrumbList

**Testo categoria esempio:**
```
I filtri olio per BMW sono componenti critici per mantenere
il motore pulito e efficiente. Sul nostro catalogo trovi filtri
OES di Elring, Corteco e Mann per tutte le Serie BMW con motori
diesel N47, B47, M57 e benzina N52, N55, B58. [...]
```

### Pagine Prodotto

**Elementi SEO critici:**
1. Title unico con keyword + modello + marca ricambio
2. Descrizione originale (NON quella del fornitore)
3. Codice OE nel testo e negli attributi
4. Lista compatibilità veicoli
5. Immagini ottimizzate con alt text
6. Schema Product con prezzo e disponibilità

**Template descrizione prodotto:**
```
[Nome prodotto] è un ricambio [qualità: OES/OEM/aftermarket] prodotto
da [marca] per [veicoli compatibili] con motore [codici motore].

Specifiche tecniche:
- Codice OE: [codice]
- Codice produttore: [codice]
- Materiale: [materiale]
- Dimensioni: [dim]

Compatibile con: [lista veicoli]

Sostituisce i codici: [cross-reference]
```

## Gestione URL Duplicate

### Filtri e Sorting
I filtri WooCommerce (per marca, prezzo, ecc.) generano URL come:
`/filtri-olio/?orderby=price&min_price=10&max_price=50`

**Soluzione:**
- Aggiungi `?` URL al robots.txt: `Disallow: /*?*` (blocca tutti i parametri)
- Oppure usa canonical tag automatico (Yoast lo gestisce)
- Non indicizzare le pagine di sorting (noindex)

### Paginazione
`/filtri-olio/page/2/`, `/filtri-olio/page/3/` ecc.

**Soluzione moderna:** canonical sulla pagina 1 per tutte le pagine di paginazione. Google capisce da solo.

## Prodotti Esauriti e Discontinuati

### Prodotto temporaneamente esaurito
- **NON rimuovere la pagina** — mantieni il ranking
- Mostra "Prodotto esaurito — avvisami quando disponibile"
- Aggiungi prodotti alternativi/correlati
- Mantieni la pagina indicizzata

### Prodotto discontinuato definitivamente
- Se hai un sostituto: 301 redirect al prodotto sostitutivo
- Se non hai sostituti: 301 redirect alla categoria
- Solo se la pagina aveva zero traffico: lascia il 404

## SEO per Varianti Prodotto

Se un prodotto ha varianti (es. ammortizzatore anteriore/posteriore):
- Crea una pagina madre con tutte le varianti (approccio WooCommerce standard)
- Oppure crea pagine separate per varianti molto diverse
- Usa canonical se le varianti hanno pagine separate

## Contenuto per Long-Tail: Il Blog

Il blog è il modo più scalabile per catturare traffico long-tail:

**Tipi di articoli ad alto valore:**
1. **Guide installazione:** "Come cambiare il filtro olio BMW E90 — Guida passo passo"
2. **Diagnosi problemi:** "Sintomi guarnizione testata rotta BMW N47"
3. **Comparativa prodotti:** "Elring vs Mann: quale filtro olio scegliere per BMW?"
4. **Guide manutenzione:** "Ogni quanti km cambiare il filtro olio BMW diesel"
5. **Guida compatibilità:** "Tutti i ricambi compatibili BMW Serie 3 E90 2005-2012"

**Struttura articolo SEO:**
- H1 con keyword principale
- Introduzione (risponde alla query in 2-3 righe)
- Sommario con anchor link
- Contenuto strutturato con H2/H3
- FAQ in fondo (ottimo per featured snippet)
- CTA ai prodotti correlati

## Rich Snippets per E-commerce

I rich snippet migliorano il CTR nei risultati Google:

- **Prezzo e disponibilità** — automatico con Product schema
- **Recensioni stelle** — aggiungi plugin recensioni (es. Trustpilot)
- **Breadcrumb** — automatico con Yoast
- **FAQ** — aggiungi FAQ schema alle pagine categoria e blog

## Checklist SEO E-commerce (Mensile)

- [ ] Search Console: nuovi errori 404?
- [ ] Nuove pagine indicizzate?
- [ ] Keyword in crescita/calo?
- [ ] Core Web Vitals: miglioramenti?
- [ ] Nuovi prodotti con descrizioni originali?
- [ ] Blog: almeno 2 nuovi articoli?
- [ ] Link building: nuovi backlink acquisiti?
