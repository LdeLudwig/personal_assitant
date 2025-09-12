import telegram
from fastapi import APIRouter, Depends, Request
from telegram import Update
from personal_notion_agent.infrastructure.settings import get_settings

manager = APIRouter()

print("Manager configurado")


@manager.post("/")
async def notion_manager(request: Request, settings=Depends(get_settings)):
    payload_dict = await request.json()

    update = Update.de_json(payload_dict, None)

    bot = telegram.Bot(settings.telegram_api_key)

    message = update.message.text
    chat_id = update.message.chat_id

    if not (update.message and message):
        print("Received an update without a message text.")
        return {"status": "ignored", "message": "No message"}

    print(f"Processing prompt for chat_id: {chat_id}")
    agent = settings.agent_factory.get_agent("manager")

    final_prompt = f"""
        Originalmente o usuário requisitou: {message}
    """

    response = await agent.arun(final_prompt)
    print(f"Resposta do agent: {response.content}")

    await bot.send_message(text=response.content, chat_id=chat_id)

    return {"status": "completed", "message": "Response sent"}


@manager.get("/test")
async def test(payload: str):
    return payload
