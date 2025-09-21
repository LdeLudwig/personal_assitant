import os
from dotenv import load_dotenv
from telegram import Bot
from agno.tools import tool

# Utils
from ..utils.group_identify import group_identify


load_dotenv()

telegram_api_key = os.getenv("TELEGRAM_API_KEY")

bot = Bot(telegram_api_key)


@tool(
    name="reply",
    description="Envia resposta para o usuário",
)
async def reply(message: str, chat_id: str):
    await bot.send_message(text=message, chat_id=chat_id)


@tool(
    name="get models",
    description="Retorna o esquema JSON dos modelos de tarefa para o banco informado.",
)
def get_models(name: str):
    group = group_identify(name)

    json_schema = group["model"].model_json_schema()

    return json_schema
