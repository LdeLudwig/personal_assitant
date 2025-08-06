import os
from pydantic import BaseModel, Field
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseModel):
    # API KEYS
    notion_api_key: str = Field(default_factory=lambda: os.getenv("NOTION_API_KEY"))
    
    # NOTION DATABASES
    personal_tasks_db_id: str = Field(default_factory=lambda: os.getenv("PERSONAL_TASKS_DB_ID"))
    work_tasks_db_id: str = Field(default_factory=lambda: os.getenv("WORK_TASKS_DB_ID"))


def get_settings() -> Settings:
    settings = Settings()
    return settings