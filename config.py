"""Configurazione centralizzata."""
import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
    MARGINE_PERCENTUALE = float(os.getenv("MARGINE_PERCENTUALE", "30"))
    ALIQUOTA_IVA = float(os.getenv("ALIQUOTA_IVA", "22"))
    HOST = os.getenv("HOST", "127.0.0.1")
    PORT = int(os.getenv("PORT", "8000"))

    # WordPress / WooCommerce
    WP_URL = os.getenv("WP_URL", "")
    WP_USER = os.getenv("WP_USER", "")
    WP_PASSWORD = os.getenv("WP_PASSWORD", "")

    # Portali B2B (credenziali per login automatico)
    # Formato: PORTALE_URL, PORTALE_USER, PORTALE_PASSWORD
    PORTALI_B2B = {
        "azcar": {
            "url": os.getenv("AZCAR_URL", ""),
            "user": os.getenv("AZCAR_USER", ""),
            "password": os.getenv("AZCAR_PASSWORD", ""),
            "nome": "AZ Car B2B",
        },
        "elring": {
            "url": os.getenv("ELRING_URL", "https://www.elring.de"),
            "user": os.getenv("ELRING_USER", ""),
            "password": os.getenv("ELRING_PASSWORD", ""),
            "nome": "Elring",
        },
        "corteco": {
            "url": os.getenv("CORTECO_URL", "https://www.corteco.com"),
            "user": os.getenv("CORTECO_USER", ""),
            "password": os.getenv("CORTECO_PASSWORD", ""),
            "nome": "Corteco",
        },
        "valeo": {
            "url": os.getenv("VALEO_URL", "https://www.valeo.com"),
            "user": os.getenv("VALEO_USER", ""),
            "password": os.getenv("VALEO_PASSWORD", ""),
            "nome": "Valeo",
        },
        "autodoc": {
            "url": os.getenv("AUTODOC_URL", "https://www.autodoc.it"),
            "user": os.getenv("AUTODOC_USER", ""),
            "password": os.getenv("AUTODOC_PASSWORD", ""),
            "nome": "AutoDoc",
        },
    }

    # Browser-use: False = mostra il browser (utile per debug), True = invisibile
    BROWSER_HEADLESS = os.getenv("BROWSER_HEADLESS", "true").lower() != "false"

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DATA_DIR = os.path.join(BASE_DIR, "data")
    EXPORTS_DIR = os.path.join(BASE_DIR, "exports")
    MEMORIA_PATH = os.path.join(DATA_DIR, "memoria.json")
    KNOW_DIR = os.path.join(BASE_DIR, "know")

    @classmethod
    def validate(cls):
        if not cls.ANTHROPIC_API_KEY:
            raise ValueError(
                "ANTHROPIC_API_KEY non configurata! "
                "Copia .env.example in .env e inserisci la tua chiave."
            )
        os.makedirs(cls.DATA_DIR, exist_ok=True)
        os.makedirs(cls.EXPORTS_DIR, exist_ok=True)
        os.makedirs(cls.KNOW_DIR, exist_ok=True)  # cartella know/ alla radice
        return True
