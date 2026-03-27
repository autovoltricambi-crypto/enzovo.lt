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

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DATA_DIR = os.path.join(BASE_DIR, "data")
    EXPORTS_DIR = os.path.join(BASE_DIR, "exports")
    MEMORIA_PATH = os.path.join(DATA_DIR, "memoria.json")

    @classmethod
    def validate(cls):
        if not cls.ANTHROPIC_API_KEY:
            raise ValueError(
                "ANTHROPIC_API_KEY non configurata! "
                "Copia .env.example in .env e inserisci la tua chiave."
            )
        os.makedirs(cls.DATA_DIR, exist_ok=True)
        os.makedirs(cls.EXPORTS_DIR, exist_ok=True)
        return True
