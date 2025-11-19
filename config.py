import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_TOKEN")
BOT_USERNAME = os.getenv("BOT_USERNAME")
TWITTER_CLIENT_KEY = os.getenv("TWITTER_CLIENT_KEY")
TWITTER_CLIENT_SECRET = os.getenv("TWITTER_CLIENT_SECRET")
TWITTER_CLIENT_ID = os.getenv("TWITTER_CLIENT_ID")
callback_url = os.getenv("CALLBACK_URL", "http://localhost:8000/callback")
fastapi_host = os.getenv("FASTAPI_HOST")
fastapi_port = int(os.getenv("FASTAPI_PORT", 8000))
