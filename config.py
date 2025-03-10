import os
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

class Config:
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    API_URL = "https://addressvalidation.googleapis.com/v1:validateAddress"

    if not GOOGLE_API_KEY:
        raise ValueError("La clé API Google est manquante. Ajoutez-la dans un fichier .env")

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False
