import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from personal_notion_agent.infrastructure.cors import setup_cors
from personal_notion_agent.routes.manager import manager

load_dotenv()

app = FastAPI()

#setup_cors(app)
print("CORS configurado com sucesso")

app.include_router(manager, prefix="/manager")

# Redirect root to docs
@app.get("/")
def docs():
    return RedirectResponse(url="/docs")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
