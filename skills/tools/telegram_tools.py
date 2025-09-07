import os
import asyncio
import telegram
import json
from dotenv import load_dotenv

load_dotenv()

token = os.getenv("TELEGRAM_API_KEY")

bot = telegram.Bot(token)


async def get_messages():
    async with bot:
        received_message = (await bot.get_updates())[0]
        print(f"messages: {json.dumps(received_message.to_dict(), indent=2)}")


async def send_messages():
    pass


if __name__ == "__main__":
    asyncio.run(get_messages())
