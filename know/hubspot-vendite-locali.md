# HubSpot + Agente Vendite Locali (WhatsApp)

## Obiettivo operativo

Gestire in modo semplice e strutturato le vendite locali tracciando:
- cliente
- numero WhatsApp
- auto possedute
- storico acquisti
- preventivi emessi e stato

L'agente deve usare i tool memoria per non perdere informazioni tra sessioni.

## Flusso consigliato in negozio

1. Nuovo cliente locale:
   - usare `salva_cliente_locale(nome, whatsapp, auto, note)`
2. Dopo una vendita:
   - usare `aggiorna_acquisto_cliente(whatsapp, descrizione_acquisto, auto, importo)`
3. Quando invii un preventivo:
   - usare `registra_preventivo(whatsapp, descrizione, auto, importo, stato="inviato")`
4. Per consultazione rapida:
   - usare `scheda_cliente(whatsapp)` oppure `lista_clienti_locali(query)`

## Mappatura minima verso HubSpot CRM

Proprietà contatto HubSpot consigliate:
- `firstname` / `lastname` oppure `name`
- `phone` (numero WhatsApp)
- `car_models` (testo multi-valore)
- `last_purchase_note`
- `last_quote_status`

Pipeline Deal HubSpot suggerita per preventivi:
- Bozza
- Inviato
- Accettato
- Rifiutato

Mappatura stato preventivo agente ↔ HubSpot:
- `bozza` → Deal stage "Bozza"
- `inviato` → Deal stage "Inviato"
- `accettato` → Deal stage "Accettato"
- `rifiutato` → Deal stage "Rifiutato"

## Note pratiche

- Usa sempre il numero WhatsApp come chiave principale per evitare duplicati.
- Quando un cliente aggiorna auto o esigenze, aggiorna subito la scheda.
- Prima di creare un nuovo preventivo, controlla `scheda_cliente` per vedere storico e trattative aperte.
