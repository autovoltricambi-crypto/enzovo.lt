# SEO Off-Page — Link Building

## Cos'è il Link Building

Il link building è il processo di acquisire backlink (link da altri siti al tuo) per aumentare l'autorità del dominio agli occhi di Google. L'autorità del dominio è uno dei fattori di ranking più importanti.

**Logica:** se molti siti autorevoli linkano il tuo sito, Google lo considera più affidabile e rilevante → ranking più alti.

**Qualità > Quantità:**
- 1 link da un sito autorevole del settore auto = 100 link da directory spam
- Google penalizza i link artificiali e comprati

## Metriche di Qualità dei Backlink

| Metrica | Tool | Significato |
|---------|------|-------------|
| **Domain Rating (DR)** | Ahrefs | Autorità del dominio 0-100 |
| **Domain Authority (DA)** | Moz | Simile al DR |
| **Topical Relevance** | Analisi manuale | Il sito è rilevante per l'auto? |
| **Traffic** | Ahrefs/Semrush | Il sito ha traffico reale? |
| **Spam Score** | Moz | Indica link spam (< 30%) |
| **Anchor Text** | Ahrefs | Testo del link |

**Target:** link da siti con DR > 30, traffico reale, rilevanti per auto/e-commerce.

## Strategie White Hat (Sicure)

### 1. Link da Fornitori

**Come ottenere:**
- Chiedi ai fornitori (Elring, Mann, Bosch) di essere listato come rivenditore sul loro sito
- Molti produttori hanno pagine "Dove Acquistare" o "Rivenditori"
- Link molto autorevoli e rilevanti

**Email di richiesta:**
```
Oggetto: Richiesta inserimento come rivenditore — [brand]

Gentili [nome],

Siamo enzovo.lt, e-commerce italiano specializzato in ricambi auto.
Offriamo i vostri prodotti [Elring/Mann/...] al mercato italiano.

Avremmo piacere di essere inseriti nella vostra pagina "Rivenditori"
o "Dove acquistare" con un link al nostro catalogo.

Potete trovarci su: enzovo.lt/ricambi/[brand]

Grazie mille,
[nome]
```

### 2. Guest Posting su Blog Auto

Scrivi articoli come ospite su blog/siti del settore auto:

**Target siti:**
- Blog meccanica (italiano)
- Riviste auto online
- Forum BMW, Fiat, VW Italia
- Blog "fai da te" auto

**Come proporre:**
```
Oggetto: Proposta articolo ospite — [argomento]

Salve [editor],

Sono [nome] di enzovo.lt. Ho letto il vostro articolo su [articolo] e
ho un'idea che potrebbe interessare i vostri lettori:

"[Titolo proposta articolo]"
[2-3 righe di presentazione del contenuto]

Offrirò un articolo originale di 1.500+ parole, ottimizzato SEO,
con immagini incluse. In cambio, mi piacerebbe includere 1-2 link
naturali al mio sito.

Siete interessati?

[Nome]
```

**Buone pratiche:**
- Il contenuto deve essere genuinamente utile per i lettori del sito ospitante
- Link naturale nel testo, non in firma o bio
- Anchor text vario (non sempre la stessa keyword)

### 3. Digital PR — Comunicati Stampa

**Come funziona:**
- Crea notizie degne di interesse per i media auto italiani
- Invia comunicato stampa ai giornalisti del settore
- Se coprono la storia → link naturale al tuo sito

**Idee notizie:**
- Dati esclusivi: "I ricambi BMW più venduti online in Italia nel 2024"
- Studio: "Il costo reale del tagliando BMW fai-da-te vs officina"
- Lancio: "Nuovo servizio compatibilità auto per targa"

**Target media:**
- Quattroruote.it
- AutoMoto.it
- MotorBox.com
- La Stampa Motori

### 4. Forum e Community

**Partecipazione autentica** (non spam):
- Forum BMW Italia, Forum Fiat, Forum VW
- Reddit r/Italy + automotive subreddit
- Community Facebook di appassionati auto

**Regola:** prima dai valore (rispondi alle domande), poi eventualmente menciona il tuo sito come risorsa dove ha senso.

**Mai:** linkare al sito a caso in ogni post → ban immediato.

### 5. Broken Link Building

Trova link rotti su siti auto italiani e proponi il tuo come sostituto:

```
Step 1: Trova siti auto con molti link in uscita
Step 2: Usa Ahrefs → "Broken Links" per trovare link rotti
Step 3: Verifica se hai contenuto equivalente sul tuo sito
Step 4: Contatta il sito segnalando il link rotto e proponendo il tuo
```

### 6. Menzioni Non Linkate (Unlinked Mentions)

Cerca il nome del tuo brand citato online senza link:
```
Google: "enzovo" OR "enzovo.lt" -site:enzovo.lt
```

Contatta chi ha menzionato il tuo sito chiedendo di aggiungere il link.

### 7. Creazione di Risorse Linkabili

Crea contenuto talmente utile che altri vogliono linkarlo spontaneamente:
- Database compatibilità ricambi (consultabile gratis)
- Calcolatore: "Quanto risparmio facendo il tagliando da solo?"
- Guida completa "Ricambi BMW E90 — Tutto quello che devi sapere"
- Infografica: "Piano manutenzione auto — quando cambiare cosa"

## Analisi Backlink Competitor

Prima di fare link building, analizza i link dei competitor:

```
In Ahrefs:
1. Inserisci URL competitor (autodoc.it, ecc.)
2. Vai su "Backlinks" → filtra per DR > 30
3. Analizza: chi li linka? Perché? Posso replicare?
4. Gap Analysis: chi linka i competitor ma non me?
```

## Link Non Desiderabili (Evitare)

- Link comprati (penalizzazione Google)
- Link da PBN (Private Blog Network)
- Link da siti spam o irrilevanti
- Scambio sistematico (A linka B, B linka A in modo artificiale)
- Anchor text sovra-ottimizzato (troppi link con keyword esatta)

## Disavow

Se hai ricevuto link spam (acquistati in passato o da attacchi negativi):
1. Vai su Google Search Console → Link Legacy → Disavow
2. Carica file txt con domini da disconoscere
3. Google non considererà quei link nel ranking

**Usare con cautela** — se fatto male può peggiorare il ranking.

## Metriche Link Building

| Metrica | Tool | Frequenza Controllo |
|---------|------|---------------------|
| Nuovi backlink acquisiti | Ahrefs | Mensile |
| Domain Rating crescita | Ahrefs | Trimestrale |
| Link persi | Ahrefs "Lost Backlinks" | Mensile |
| Anchor text distribution | Ahrefs | Trimestrale |
| Traffico referral | GA4 | Mensile |

## Checklist Link Building

- [ ] Analisi backlink competitor completata
- [ ] Lista siti target (fornitori, blog, forum) definita
- [ ] Email template guest posting pronta
- [ ] Richiesta a fornitori come rivenditore inviata
- [ ] Partecipazione autentica a 2-3 forum settore
- [ ] Almeno 1 risorsa linkabile creata
- [ ] Monitoraggio mensile nuovi link (Ahrefs alert)
- [ ] Disavow link spam se necessario
- [ ] Profilo anchor text naturale (no keyword stuffing)
