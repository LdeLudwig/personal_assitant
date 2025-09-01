from fastapi import APIRouter, Depends, BackgroundTasks
from personal_notion_agent.infrastructure.settings import get_settings

manager = APIRouter()

async def request_processor(payload: str, settings):
    agent = settings.agent_factory.get_agent("manager")

    final_prompt = f"""
        Originalmente o usuário requisitou: {payload}
    """

    response = await agent.arun(final_prompt)
    return response.content


@manager.post("/")
async def notion_manager(
    payload: str,
    background_tasks: BackgroundTasks,
    settings=Depends(get_settings)
):
    background_tasks.add_task(request_processor, payload, settings)
    return {"status": "processing", "message": "Your request is been processed"}


