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
    name="get_models",
    description="Retorna o esquema JSON dos modelos de tarefa para o banco informado.",
)
def get_models(name: str):
    """Retorna o JSON Schema do modelo do grupo informado.

    Regras:
    - Aceita somente: "pessoal", "trabalho", "projetos" (inclui sinônimos comuns).
    - Para nomes inválidos, retorna a string: "ERROR: grupo inválido".
    """

    group = group_identify(name)
    try:
        json_schema = group
        return json_schema
    except Exception:
        return "ERROR: grupo inválido"
