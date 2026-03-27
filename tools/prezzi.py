"""Calcolo prezzi: margine e IVA."""
from config import Config


def calcola_prezzo_vendita(
    costo: float,
    margine: float = None,
    iva: float = None,
) -> dict:
    """
    Calcola il prezzo di vendita finale partendo dal costo fornitore.
    prezzo_vendita = costo * (1 + margine/100) * (1 + iva/100)
    """
    if margine is None:
        margine = Config.MARGINE_PERCENTUALE
    if iva is None:
        iva = Config.ALIQUOTA_IVA

    prezzo_netto = round(costo * (1 + margine / 100), 2)
    prezzo_finale = round(prezzo_netto * (1 + iva / 100), 2)

    return {
        "costo_fornitore": round(costo, 2),
        "margine_percentuale": margine,
        "prezzo_netto": prezzo_netto,
        "iva_percentuale": iva,
        "prezzo_finale_ivato": prezzo_finale,
        "guadagno_netto": round(prezzo_netto - costo, 2),
    }


def scorporo_iva(prezzo_ivato: float, iva: float = None) -> dict:
    """
    Estrae il prezzo netto da un prezzo IVA inclusa.
    prezzo_netto = prezzo_ivato / (1 + iva/100)
    """
    if iva is None:
        iva = Config.ALIQUOTA_IVA

    prezzo_netto = round(prezzo_ivato / (1 + iva / 100), 2)
    iva_importo = round(prezzo_ivato - prezzo_netto, 2)

    return {
        "prezzo_ivato": round(prezzo_ivato, 2),
        "iva_percentuale": iva,
        "prezzo_netto": prezzo_netto,
        "iva_importo": iva_importo,
    }
