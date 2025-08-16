import os
from functools import lru_cache
from pydantic import BaseModel, Field
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseModel):
    # API KEYS
    notion_api_key: str = Field(default_factory=lambda: os.getenv("NOTION_API_KEY"))
    open_router_api_key: str = Field(default_factory=lambda: os.getenv("OPENROUTER_API_KEY"))
    
    # NOTION DATABASES
    """ project_db_id: str = Field(default_factory=lambda: os.getenv("PROJECTS_DB_ID"))
    personal_tasks_db_id: str = Field(default_factory=lambda: os.getenv("PERSONAL_TASKS_DB_ID"))
    work_tasks_db_id: str = Field(default_factory=lambda: os.getenv("WORK_TASKS_DB_ID")) """
    
    # Model
    gemini_pro_model: str = Field(default_factory=lambda: os.getenv("GIMINI_PRO_MODEL"))
    
    # Temperature
    temperature: str = Field(default_factory=lambda: os.getenv("TEMPERATURE"))

@lru_cache()
def get_settings() -> Settings:
    settings = Settings()
    return settings