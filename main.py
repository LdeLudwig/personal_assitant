import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from personal_notion_agent.infrastructure.cors import setup_cors
from personal_notion_agent.routes.bullet_journal import bullet_journal

load_dotenv()

app = FastAPI()

setup_cors(app)
print("CORS configurado com sucesso")

app.include_router(bullet_journal, prefix="/bullet_journal")

# Redirect root to docs
@app.get("/")
def docs():
    return RedirectResponse(url="/docs")

if __name__ == "__main__":
    uvicorn.run("main:main", host="0.0.0.0", port=8000, reload=True)
