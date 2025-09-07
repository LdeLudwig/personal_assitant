import os
from functools import lru_cache
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from personal_notion_agent.app.agent_factory import AgentFactory


load_dotenv()


class Settings(BaseModel):
    # API KEYS
    notion_api_key: str = Field(default_factory=lambda: os.getenv("NOTION_API_KEY"))
    open_router_api_key: str = Field(
        default_factory=lambda: os.getenv("OPENROUTER_API_KEY")
    )
    gemini_api_key: str = Field(default_factory=lambda: os.getenv("GEMINI_API_KEY"))

    # NOTION DATABASES
    project_db_id: str = Field(default_factory=lambda: os.getenv("PROJECTS_DB_ID"))
    personal_tasks_db_id: str = Field(
        default_factory=lambda: os.getenv("PERSONAL_TASKS_DB_ID")
    )
    work_tasks_db_id: str = Field(default_factory=lambda: os.getenv("WORK_TASKS_DB_ID"))

    # telegram
    telegram_api_key: str = Field(default_factory=lambda: os.getenv("TELEGRAM_API_KEY"))

    # Model
    gemini_pro_model: str = Field(default_factory=lambda: os.getenv("GIMINI_PRO_MODEL"))

    # Temperature
    temperature: float = Field(default_factory=lambda: float(os.getenv("TEMPERATURE")))

    # CORS defaults
    cors_allowed_origins: list[str] = Field(
        default_factory=lambda: os.getenv("CORS_ALLOWED_ORIGINS", "*").split(",")
    )
    cors_allowed_methods: list[str] = Field(
        default_factory=lambda: os.getenv("CORS_ALLOWED_METHODS", "*").split(",")
    )
    cors_allowed_headers: list[str] = Field(
        default_factory=lambda: os.getenv("CORS_ALLOWED_HEADERS", "*").split(",")
    )
    cors_allow_credentials: bool = Field(
        default_factory=lambda: os.getenv("CORS_ALLOW_CREDENTIALS", "false").lower()
        in ("1", "true", "yes")
    )
    cors_expose_headers: list[str] = Field(
        default_factory=lambda: [
            h for h in os.getenv("CORS_EXPOSE_HEADERS", "").split(",") if h
        ]
    )

    # Placeholder for runtime-initialized factory
    agent_factory: object | None = None

    # Initialize agent factory lazily to avoid circular import
    def model_post_init(self, __context: None):
        self.agent_factory = AgentFactory(self)


@lru_cache()
def get_settings() -> Settings:
    settings = Settings()
    return settings
