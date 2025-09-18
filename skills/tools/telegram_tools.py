import os
from dotenv import load_dotenv
from telegram import Bot

load_dotenv()

telegram_api_key = os.getenv("TELEGRAM_API_KEY")


bot = Bot(telegram_api_key)


def reply():
    pass


def get_create_models():
    pass
