# Scraping Web — Strategia Operativa

## Obiettivo

Fare scraping in modo pragmatico scegliendo il tool giusto: browser-use per esplorare,
Playwright per estrarre in modo strutturato, ripetibile e più preciso.

---

## Regola Base

Non usare sempre lo stesso approccio.

### Usa browser-use quando:
- il sito è sconosciuto
- serve capire il flusso visivo
- ci sono login, popup, cookie banner, menu, ricerca interna
- devi esplorare prima di decidere come estrarre i dati

### Usa Playwright quando:
- hai già capito la struttura della pagina
- vuoi estrarre liste, card, articoli, prodotti, righe tabella
- vuoi risultati più ripetibili e meno interpretativi
- devi leggere siti renderizzati in JavaScript

---

## Workflow Consigliato

1. `naviga_web(url, obiettivo)`
2. `analizza_struttura_pagina(url)`
3. `estrai_dati_con_playwright(url, selettori, limite)`

---

## Quando consultare questo file

Leggere questo file se il task riguarda:
- scraping siti sconosciuti
- passaggio da esplorazione visiva a estrazione strutturata
- scelta tra browser-use e Playwright
- estrazione di card, articoli, prodotti o tabelle da pagine web