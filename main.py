import os
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from personal_notion_agent.routes.bullet_journal import bullet_journal


app = FastAPI()

app.include_router(bullet_journal, prefix="/bullet_journal")

# Redirect root to docs
@app.get("/")
def docs():
    return RedirectResponse(url="/docs")
