from fastapi import APIRouter, Depends, Request
from telegram import Update
from personal_notion_agent.infrastructure.settings import get_settings

manager = APIRouter()


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
            O chat_id do usuário é: {chat_id}
            
        """
        response = await coordinator.arun(final_prompt)
        print(f"Resposta do coordinator: {response.content}")

    except Exception as e:
        print(f"An error occurred: {e}")

    return {"status": "completed", "message": "Response sent"}


@manager.get("/test_manager")
async def test(request: str, chat_id: str, settings=Depends(get_settings)):
    try:
        coordinator = settings.agent_factory.get_agent("coordinator")

        final_prompt = f"""
            Originalmente o usuário requisitou: {request}
            O chat_id do usuário é: {chat_id}
        """
        response = await coordinator.arun(final_prompt)
        print(f"Resposta do agent: {response.content}")
    except Exception as e:
        print(f"An error occurred: {e}")

    return {"status": "completed", "message": "Response sent"}
