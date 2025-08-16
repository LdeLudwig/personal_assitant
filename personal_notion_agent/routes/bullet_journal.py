from fastapi import APIRouter, Depends, BackgroundTasks
from personal_notion_agent.infrastructure.settings import get_settings

bullet_journal = APIRouter()

async def request_processor():
    pass



@bullet_journal.post
async def notion_manager(
    payload: str,
    background_tasks: BackgroundTasks,
    settings=Depends(get_settings)
):
    pass


