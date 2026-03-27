# E-commerce — Retention e Fidelizzazione Clienti

## Perché la Retention è Più Importante dell'Acquisizione

**Dati:**
- Acquisire un nuovo cliente costa 5-7x più che mantenerne uno esistente
- Aumentare la retention del 5% → profitti +25-95%
- Clienti abituali spendono in media il 67% in più dei nuovi clienti
- Il 65% del fatturato di un e-commerce maturo viene da clienti esistenti

**Per ricambi auto:** un cliente che ha comprato un filtro olio per la sua BMW probabilmente avrà bisogno di altri ricambi per la stessa auto ogni 6-12 mesi. Se la sua prima esperienza è positiva, è quasi certo che torni.

## Metriche di Retention

| Metrica | Formula | Target |
|---------|---------|--------|
| **Repeat Purchase Rate** | Clienti con 2+ ordini / Totale clienti | > 30% |
| **Customer Retention Rate** | (Clienti fine - Nuovi) / Clienti inizio | > 60% |
| **Churn Rate** | Clienti persi / Clienti totali | < 20%/anno |
| **Purchase Frequency** | Ordini totali / Clienti unici | > 1.5/anno |
| **Time Between Purchases** | Media giorni tra acquisti | < 120 giorni |

## Programma Fedeltà

### Modello Punti
```
€1 speso = 1 punto
100 punti = €1 di sconto
Bonus: +50 punti per recensione, +100 per primo ordine
```

**Plugin WooCommerce:** WooCommerce Points and Rewards.

### Modello a Livelli (Tier)
```
Bronzo: 0-199€ spesi/anno → spedizione standard, -5%
Argento: 200-499€ → spedizione gratuita, -10%
Oro: 500€+ → priorità assistenza, -15%, accesso offerte early
```

### Modello Abbonamento
Per ricambi con ricambio periodico prevedibile:
```
"Abbonamento tagliando BMW"
- Ogni 12 mesi: filtro olio + filtro aria consegnati automaticamente
- Sconto 15% rispetto all'acquisto singolo
- Nessun pensiero: ricevi i prodotti quando servono
```

**Vantaggio:** LTV garantito, cash flow prevedibile.

## Email Retention

### Ciclo Vita Post-Acquisto

```
Giorno 1: Conferma ordine + info spedizione
Giorno 3-5: Email "Come stai?" + link tutorial installazione
Giorno 10: Richiesta recensione
Giorno 30: Cross-sell (prodotti complementari)
Giorno 90: Reminder manutenzione ("È passato 1 trimestre — controlla i livelli")
Giorno 180: Reminder "E se cambiassi il filtro aria?"
Giorno 365: Anniversario + offerta esclusiva
```

### Email Personalizzate per Modello Auto

Se raccogli il modello auto al checkout:
```python
# Logica automazione
SE cliente.acquistato == "filtro_olio_bmw_n47":
    DOPO 12_MESI: invia email
    oggetto = "È ora del tagliando per la tua BMW?"
    prodotti = filtri compatibili BMW N47
    link = pagina categoria BMW
```

## Assistenza Clienti come Retention Tool

L'assistenza è uno dei driver di retention più potenti. Un cliente con problema risolto velocemente è più fedele di uno che non ha mai avuto problemi.

**Canali:**
- Chat live (Tidio, Crisp — gratuito)
- WhatsApp Business
- Email support con SLA di risposta (< 4h)
- FAQ completa

**Per ricambi auto — domande frequenti:**
- "È compatibile con la mia auto?"
- "Come si installa?"
- "Ho ordinato il prodotto sbagliato — posso cambiarlo?"
- "Quando arriva?"

**Knowledge base:** crea FAQ categorizzata. Riduce carico assistenza e migliora SEO.

## Reso Facile = Più Vendite

Un processo di reso semplice e gratuito aumenta le conversioni del 20-30%.

**Policy ottimale:**
- 30 giorni per il reso
- Reso gratuito (o etichetta prepagata)
- Rimborso entro 5 giorni
- Processo online semplice (non "chiama il lunedì 9-12")

**Paradosso:** chi usa facilmente il reso, acquista di più nel lungo termine.

## Social Proof e Comunità

### Recensioni
- Chiedi recensioni via email post-acquisto (giorno 10-14)
- Rispondi a TUTTE le recensioni (positive e negative)
- Mostra le recensioni su pagine prodotto e Google Shopping

**Platform:**
- Google Business Profile (recensioni Google — le più importanti)
- Trustpilot (credibilità alta, visibile su Google)
- Recensioni WooCommerce native

### Referral Program
"Porta un amico" — il word of mouth più potente:
```
Tu inviti un amico → lui ottiene 10% primo acquisto
→ Tu ottieni €10 di credito quando lui ordina
```

**Plugin:** ReferralCandy, Yithemes Referral.

### Social Media Comunità
Gruppo Facebook/Telegram per clienti:
- "BMW Owners Italia" — crea contenuto, FAQ, sconti esclusivi
- Rafforza brand, crea community, ottieni UGC (user generated content)

## Remarketing per Clienti Esistenti

**Google Ads:**
- Lista "Clienti" in remarketing → mostra prodotti complementari
- Escludi da campagne acquisizione (non sprecare budget)

**Meta Ads:**
- Custom Audience: lista email clienti
- Mostra ads prodotti che non hanno ancora comprato ma hanno visualizzato

**Email:**
- Segmento "At Risk" (non compra da 90gg) → win-back campaign
- Segmento "Champions" → early access a nuovi prodotti

## Surprise & Delight

Elementi inaspettati che creano WOW e fidelizzano:

- **Nota scritta a mano** nel pacco (scalabile con template)
- **Campione omaggio** (prodotto secondario incluso)
- **Upgrade spedizione** a sorpresa per ordini importanti
- **Coupon esclusivo** per clienti fedeli senza che l'abbiano chiesto
- **Email di compleanno** con sconto

Costo marginale basso, impatto sulla fedeltà molto alto.

## Checklist Retention

- [ ] Programma fedeltà configurato (punti o livelli)
- [ ] Flusso email post-acquisto completo
- [ ] Email personalizzate per marca auto del cliente
- [ ] Flusso win-back configurato (90 giorni inattività)
- [ ] Policy reso chiara e semplice visibile
- [ ] Sistema recensioni automatizzato
- [ ] Risposta a tutte le recensioni Google
- [ ] Referral program configurato
- [ ] Metriche retention monitorate mensilmente (RPR, churn)
