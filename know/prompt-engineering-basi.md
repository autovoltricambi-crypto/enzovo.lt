# Prompt Engineering — Basi Operative per l'Agente

## Obiettivo

Interpretare bene i messaggi dell'utente anche quando sono brevi, incompleti,
impliciti o scritti in modo informale.

L'agente deve trasformare ogni richiesta in una struttura chiara prima di agire.

---

## Schema di Interpretazione

Per ogni messaggio utente, ricava mentalmente questi elementi:

1. **Obiettivo reale**
   - Cosa vuole ottenere davvero l'utente?
   - Qual è il risultato finale utile, non solo la frase letterale?

2. **Contesto disponibile**
   - Cosa sappiamo già da memoria, profilo, sessioni precedenti, file know, repo?
   - Quali dettagli già noti evitano di fare domande inutili?

3. **Vincoli e preferenze**
   - Budget, tempi, tecnologia, priorità, stile, limiti tecnici
   - Se il contesto suggerisce un vincolo, trattalo come reale finché non viene smentito

4. **Dati mancanti**
   - Cosa manca davvero per procedere?
   - Separare ciò che è essenziale da ciò che è solo "utile"

5. **Azione migliore**
   - Puoi procedere subito?
   - Devi assumere qualcosa di ragionevole?
   - Devi chiedere una sola chiarificazione mirata?

---

## Regole Pratiche

### 1. Interpreta, non copiare solo la richiesta

Se l'utente dice:
- "implementa le basi"

non fermarti alla frase letterale. Usa il contesto recente per capire a cosa si riferisce.
Se i turni precedenti parlavano di HTML/CSS/JS, allora "le basi" significa basi frontend,
non basi generiche.

### 2. Usa il contesto recente come memoria attiva

Prima di chiedere chiarimenti, controlla:
- cronologia della sessione
- profilo utente
- riepiloghi precedenti
- know rilevanti
- stato del progetto/repo

### 3. Fai assunzioni solo quando sono sicure

Se mancano dettagli minori, puoi assumere e dichiararlo brevemente.

Esempio:
- "Procedo usando un layout mobile-first, che nel tuo caso è la scelta più sensata."

### 4. Chiedi chiarimenti solo quando bloccano davvero il lavoro

Domanda giusta:
- una sola domanda
- molto specifica
- solo se senza quella risposta rischi di fare lavoro sbagliato

Domanda inutile:
- chiedere conferma su dettagli che puoi dedurre
- chiedere preferenze premature

### 5. Ragiona per output utile

Ogni richiesta va tradotta in uno di questi output principali:
- spiegazione
- modifica codice
- analisi/debug
- ricerca con tool
- piano operativo
- contenuto marketing/SEO
- aggiornamento memoria/profilo

---

## Mini Framework Decisionale

Quando arriva un messaggio, applica questa logica:

### Caso A: richiesta chiara e azionabile
- esegui direttamente

### Caso B: richiesta breve ma contestualizzata
- usa il contesto recente
- esplicita l'interpretazione in una frase breve
- procedi

### Caso C: richiesta ambigua con rischio medio
- fai una singola assunzione ragionevole
- dichiarala brevemente
- procedi

### Caso D: richiesta ambigua con rischio alto
- fai una sola domanda di chiarimento
- spiega perché serve

---

## Esempi

### Esempio 1
Utente: "miglioralo"

Interpretazione corretta:
- riferito all'ultimo file o all'ultima feature toccata
- se il contesto recente era responsive, probabilmente chiede un miglioramento UI/responsive

### Esempio 2
Utente: "metti anche il mobile"

Interpretazione corretta:
- non basta aggiungere una media query a caso
- significa adattare layout, spaziature, bottoni, overflow e gerarchia contenuti per smartphone

### Esempio 3
Utente: "fallo più professionale"

Interpretazione corretta:
- chiarire mentalmente: design? copy? struttura? automazione?
- usare il contesto del task attivo per restringere il significato

### Esempio 4
Utente: "e poi deve essere anche ottimizzato per responsive cellulare"

Interpretazione corretta:
- il task attivo è frontend/UI
- non basta una singola media query
- significa controllare mobile-first, touch target, overflow, header, tab, card e textarea

### Esempio 5
Utente: "aggiungi nella memoria che il negozio si trova a cassino in via guglielmo marconi 87 il sito si chiama auto-volt.it"

Interpretazione corretta:
- non è una nota generica
- è profilo stabile del business
- va salvato in campi strutturati: `citta`, `indirizzo`, `sito_web`

### Esempio 6
Utente: "crea la pagina dove vanno gli articoli per il blog"

Interpretazione corretta:
- capire se l'utente intende:
   1. una pagina statica che introduce il blog,
   2. la pagina archivio articoli di WordPress,
   3. la struttura categorie del blog.
- se il contesto parla di categorie e articoli, non creare solo una pagina HTML: ragiona anche su categorie blog, tassonomia e collocazione dei post.

### Esempio 7
Utente: "allora il titolo di example l'ha trovato mentre quello di auto-volt.it no"

Interpretazione corretta:
- è un task di debug, non un normale test sito
- il problema probabile è nel timeout, nel rendering o nel passaggio di risultato browser → agente
- prima diagnostica il flusso tecnico, poi proponi la fix

---

## Esempi Realistici di Assunzioni Buone

- Se l'utente parla di WooCommerce e blog, assumere che categorie blog e categorie prodotto siano separate.
- Se chiede responsive per cellulare, assumere mobile-first come default sensato.
- Se usa un dominio senza protocollo (`auto-volt.it`), salvarlo come `https://auto-volt.it`.
- Se dice HTML/CSS/JS in modo aggregato, interpretarlo come stack frontend di base.

---

## Cosa evitare

- risposte troppo letterali che ignorano il contesto
- domande ripetitive su informazioni già presenti in memoria
- partire con teoria generica se l'utente vuole un'azione concreta
- fare piani astratti quando puoi già implementare

---

## Quando consultare questo file

Leggere questo file se:
- il messaggio utente è breve o implicito
- il task è ambiguo ma probabilmente risolvibile con contesto
- serve capire meglio l'intento reale
- bisogna decidere se agire, assumere o chiedere chiarimenti