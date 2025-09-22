from fastapi import APIRouter, Depends, Request
from telegram import Bot, Update
from telegram.request import HTTPXRequest
from personal_notion_agent.infrastructure.settings import get_settings

manager = APIRouter()

settings = get_settings()
trequest = HTTPXRequest(connection_pool_size=50)
bot = Bot(settings.telegram_api_key, request=trequest)


@manager.post("/")
async def notion_manager(request: Request, settings=Depends(get_settings)):
    try:
        payload_dict = await request.json()

        update = Update.de_json(payload_dict, None)
        message = update.message.text
        chat_id = update.message.chat_id

        if not (update.message and message):
            print("Received an update without a message text.")
            return {"status": "ignored", "message": "No message"}

        coordinator = settings.agent_factory.get_agent("coordinator")

        final_prompt = f"""
            Originalmente o usuário requisitou: {message}            
        """
        response = await coordinator.arun(final_prompt)
        print(f"Resposta do coordinator: {response.content}")

        await bot.send_message(chat_id=chat_id, text=response.content)

    except Exception as e:
        print(f"An error occurred: {e}")

    return {"status": "completed", "message": "Response sent"}


@manager.get("/test_manager")
async def test(request: str, chat_id: str, settings=Depends(get_settings)):
    try:
        coordinator = settings.agent_factory.get_agent("coordinator")

        final_prompt = f"""
            Originalmente o usuário requisitou: {request}
        """
        response = await coordinator.arun(final_prompt)

        await bot.send_message(chat_id=chat_id, text=response.content)
        print(f"Resposta do agent: {response.content}")
    except Exception as e:
        print(f"An error occurred: {e}")

    return {"status": "completed", "message": "Response sent"}
