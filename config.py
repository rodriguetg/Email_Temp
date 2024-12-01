import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Configuration générale
    SECRET_KEY = os.getenv('SECRET_KEY', os.urandom(24))
    DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///hub.db')
    REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/0')

    # API Keys pour les différentes plateformes
    TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
    DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
    SLACK_TOKEN = os.getenv('SLACK_TOKEN')
    TWITTER_API_KEY = os.getenv('TWITTER_API_KEY')
    TWITTER_API_SECRET = os.getenv('TWITTER_API_SECRET')
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

    # Configuration des timeouts
    MESSAGE_TIMEOUT = 3600  # 1 heure
    RESPONSE_TIMEOUT = 300  # 5 minutes

    # Limites
    MAX_FILE_SIZE = 50 * 1024 * 1024  # 50 MB
    MAX_CHANNELS_PER_USER = 10
    MAX_RULES_PER_USER = 20

    # Paramètres de sécurité
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'doc', 'docx'}
    ENCRYPTION_KEY = os.getenv('ENCRYPTION_KEY', os.urandom(32))

    # Configuration des réponses automatiques
    AUTO_RESPONSE_DELAY = 60  # 1 minute
    MAX_AUTO_RESPONSES = 5
