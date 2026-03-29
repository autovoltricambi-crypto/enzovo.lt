# Blog SEO Ricambi Auto — Guida alla Creazione Articoli

## Obiettivo

Creare articoli blog che si posizionino su Google per intercettare chi cerca ricambi.
Ogni articolo deve portare traffico qualificato che poi compra dal negozio.

---

## Tipi di Articoli che Funzionano

### 1. Guide "Quale [ricambio] per [auto]"
**Template:** "Quale filtro olio per Fiat Panda 1.2? Guida completa"
- Volume ricerca alto
- Intento d'acquisto diretto
- Collega i prodotti dal negozio nell'articolo

**Struttura:**
```
H1: Quale [ricambio] per [marca] [modello] [motore]? Guida completa [anno]
H2: Che [ricambio] monta la [marca] [modello]?
  → Codice OE originale, specifiche tecniche
H2: Migliori [ricambio] aftermarket per [marca] [modello]
  → Lista prodotti con prezzi dal nostro negozio
H2: Come scegliere il [ricambio] giusto
  → Consigli, cosa guardare, errori da evitare
H2: Come sostituire il [ricambio] (opzionale, in breve)
  → Passi base, quando andare dal meccanico
H2: Domande frequenti (FAQ)
  → Schema FAQ per rich snippet Google
```

### 2. Articoli "Codice OE [codice] — Cosa è e quali alternative"
**Template:** "Codice OE 11427566327 — Filtro olio BMW: alternative compatibili"
- Intercetta chi cerca il codice specifico
- Traffico molto qualificato (sa già cosa vuole)
- Cross-reference come contenuto principale

### 3. Guide per problema/sintomo
**Template:** "Spia olio accesa Fiat Punto: cause e soluzione"
- Intercetta chi ha un problema e cerca la soluzione
- Porta al prodotto come soluzione
- Buon contenuto per SEO informativa

### 4. Confronti marca
**Template:** "Mann vs UFI vs Mahle: quale filtro olio scegliere?"
- Aiuta chi è indeciso sulla marca
- Ottimo per long-tail keywords
- Mostra competenza = fiducia

---

## Regole SEO per Ogni Articolo

### Titolo (H1 e title tag)
- Parola chiave principale all'inizio
- Max 60 caratteri per il title tag
- Includi marca + modello auto se specifico

### URL (slug)
- Breve, con parole chiave: `filtro-olio-fiat-panda-1-2`
- No stopwords, no date, no ID

### Excerpt (meta description)
- Max 155 caratteri
- Includi parola chiave + call to action
- Es: "Scopri quale filtro olio serve alla tua Fiat Panda 1.2 69cv. Codice OE, alternative aftermarket e prezzi. Spedizione rapida."

### Contenuto
- Minimo 800 parole per articoli informativi
- Minimo 500 per schede prodotto/confronto
- Includi codici OEM nel testo (sono keyword ad alto valore)
- Usa H2 e H3 con parole chiave varianti
- Link interni ai prodotti del negozio

### Categorie blog suggerite
- **Guide Ricambi** — guide "quale ricambio per quale auto"
- **Manutenzione Auto** — guide montaggio, intervalli tagliando
- **Confronti e Recensioni** — confronti marca, recensioni
- **Codici OE** — articoli su codici specifici

### Tag suggeriti
- Marca auto (fiat, bmw, volkswagen)
- Tipo ricambio (filtro-olio, pastiglie-freno)
- Modello auto (panda, golf, serie-3)

---

## SEO Locale

Per un negozio fisico/online con zona specifica:
- Includi la città nell'articolo: "Filtro olio Fiat Panda — disponibile a [città] con consegna rapida"
- Crea articoli tipo: "Ricambi auto [città]: il tuo negozio online di fiducia"
- Google My Business deve essere collegato al sito

---

## Workflow Creazione Articolo

1. Scegli il tipo di articolo (guida, codice OE, problema, confronto)
2. Consulta i know SEO: `leggi_knowledge("seo-keyword-research.md")`, `leggi_knowledge("seo-on-page.md")`
3. Identifica i prodotti collegati nel negozio
4. Scrivi il contenuto seguendo la struttura sopra
5. `crea_post_blog(titolo, contenuto_html, slug, stato="draft", categoria, tags, excerpt)`
6. Revisiona con l'utente prima di pubblicare
7. Dopo pubblicazione, salva nota con `salva_nota("Articolo pubblicato: [titolo]", "URL: ...")`
