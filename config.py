import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_TOKEN")
BOT_USERNAME = os.getenv("BOT_USERNAME")

CLIENT_SECRET = os.getenv("TWITTER_CLIENT_SECRET")
CLIENT_ID = os.getenv("TWITTER_CLIENT_ID")

BASE_SERVER_URL = os.getenv("BASE_SERVER_URL")
REDIRECT_URI = f"{BASE_SERVER_URL}/callback"

INTERNAL_API_KEY = os.getenv("INTERNAL_API_KEY")