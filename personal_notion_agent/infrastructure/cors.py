from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from personal_notion_agent.infrastructure.settings import get_settings


def setup_cors(app: FastAPI) -> None:
    settings = get_settings()
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_allowed_origins,
        allow_methods=settings.cors_allowed_methods,
        allow_headers=settings.cors_allowed_headers,
        allow_credentials=settings.cors_allow_credentials,
        expose_headers=settings.cors_expose_headers,
    )