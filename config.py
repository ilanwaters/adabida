import os
from dotenv import load_dotenv

# Carregar variables del fitxer .env
if os.getenv('FLASK_ENV') == 'production':
    load_dotenv('.env.production')
else:
    load_dotenv('.env')  # Local

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "clau-secreta-abadia")

    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        raise RuntimeError("⚠️ ERROR: Falta la variable d'entorn DATABASE_URL. Comprova el fitxer .env.")

    SQLALCHEMY_DATABASE_URI = db_url
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    STORAGE_ROOT = os.environ.get("ADABIDA_STORAGE_ROOT") or os.path.abspath(
        os.path.join(os.path.dirname(__file__), "umberto")
    )
    
    # ===== CONFIGURACIÓ EMAIL ===== (DINS de la classe!)
    MAIL_SERVER = 'mail.gandi.net'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME = 'noreply@adabida.cat'
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = ('Adabida', 'noreply@adabida.cat')
    BASE_URL = os.getenv('BASE_URL', 'http://localhost:5000')
    TOKEN_EXPIRATION_HOURS = int(os.getenv('TOKEN_EXPIRATION_HOURS', 24))
    
    # ===== IDIOMES DISPONIBLES =====
    IDIOMES_DISPONIBLES = ['ca', 'es', 'en', 'ru', 'uk', 'de', 'fr', 'eu']
    
    # Noms humans per cada idioma (per mostrar al formulari)
    IDIOMES_NOMS = {
        'ca': 'Català',
        'es': 'Español',
        'en': 'English',
        'ru': 'Русский',
        'uk': 'Українська',
        'de': 'Deutsch',
        'fr': 'Français',
        'eu': 'Euskara'
    }
    
    RTL_LANGS = {"he", "ar"}

