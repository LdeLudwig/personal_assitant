## Personal Notion Agent

FastAPI backend that orchestrates an agentic workflow to manage Notion tasks and interact via Telegram. A small team of AI agents (Coordinator, Manager, Formatter, Telegram) is powered through OpenRouter/Gemini and tool integrations for Notion and Telegram.

### Highlights
- FastAPI app with OpenAPI docs
- Agent team built with `agno` and OpenRouter models
- Tools for Notion: list, create, find, update tasks
- Telegram webhook endpoint to receive messages and send replies
- Deployable on Vercel (Python runtime)

---

## Architecture
- Entry point: `main.py`
  - Includes router under `/manager`
  - Health check at `/api/health`
  - Swagger UI at `/docs`
- Settings: `personal_notion_agent/infrastructure/settings.py`
  - Loads env vars and wires an `AgentFactory`
- Agents: `personal_notion_agent/app/agent_factory.py`
  - Manager Agent: executes Notion tools
  - Telegram Agent: provides JSON schemas (no messaging)
  - Formatter Agent: formats user-facing replies
  - Coordinator Team: orchestrates the above
- Routes: `personal_notion_agent/routes/manager.py`
  - POST `/manager/`: Telegram webhook (expects Telegram Update JSON)
  - GET `/manager/test_manager`: manual test sending a message to a `chat_id`
- Tools: `skills/tools/`
  - Notion: `list_tasks`, `create_new_tasks`, `find_task_by_title`, `find_task_by_id`, `update_task`
  - Telegram: `get_models` (returns task model JSON schema)
- Models: `personal_notion_agent/models/personal_task_model.py`
  - Validates input and builds Notion payloads
- Deployment: `vercel.json` routes all traffic to `main.py` and sets `APP_MODULE=main:app`

---

## Requirements
- Python 3.12+
- Notion internal integration and database(s)
- API keys/tokens (see Environment Variables)
- Optional: `uv` (recommended) or `pip` for dependency management

Dependencies are declared in `pyproject.toml` (locked in `uv.lock`).

---

## Setup

### 1) Create environment and install deps
- With uv (recommended):
  1. Install uv: `pipx install uv` (or `pip install uv`)
  2. Create and sync venv: `uv sync`
  3. Activate: `source .venv/bin/activate`

- With pip:
  1. Create venv: `python -m venv .venv && source .venv/bin/activate`
  2. Install: `pip install -e .`

### 2) Environment Variables
Create a `.env` file in the project root:

```
# Core APIs
NOTION_API_KEY=secret_notion_api_key
OPENROUTER_API_KEY=secret_openrouter_api_key
GEMINI_API_KEY=secret_gemini_api_key
TELEGRAM_API_KEY=secret_telegram_bot_token

# Model selection (examples; set according to your account)
GEMINI_PRO_MODEL=
GEMINI_FLASH_MODEL=
GEMINI_PRO_MODEL_OR=
GEMINI_FLASH_MODEL_OR=

# Generation controls
TEMPERATURE=0.3

# CORS (defaults shown; comma-separated values)
CORS_ALLOWED_ORIGINS=*
CORS_ALLOWED_METHODS=*
CORS_ALLOWED_HEADERS=*
CORS_ALLOW_CREDENTIALS=false
CORS_EXPOSE_HEADERS=
```

Notion database mapping: configure your database IDs and model mapping in `skills/utils/group_identify.py` so tools know which database to use for each group (e.g., "pessoal", "trabalho", "projetos"). Ensure your Notion integration has access to those databases.

### 3) Run locally
- Using Python: `python main.py`
- Or with Uvicorn: `uvicorn main:app --reload`

Docs: http://localhost:8000/docs

Health: http://localhost:8000/api/health

---

## Endpoints
- POST `/manager/`
  - Body: Telegram Update JSON
  - Behavior: Extracts message text and `chat_id`, runs the agent flow, and sends a Telegram reply
- GET `/manager/test_manager`
  - Query: `request=<text>&chat_id=<telegram_chat_id>`
  - Behavior: Triggers the agent and sends the response to `chat_id` (useful for local testing)
- GET `/api/health`
  - Returns `{ "status": "healthy" }`

---

## Telegram Webhook Setup
1. Create a bot with BotFather and copy `TELEGRAM_API_KEY`.
2. Deploy this app (or tunnel locally) and set the webhook to `https://<your-domain>/manager/`.
   - Example: `https://api.telegram.org/bot<TELEGRAM_API_KEY>/setWebhook?url=https://<your-domain>/manager/`
3. Send messages to your bot; they will be processed and answered by the agents.

Tip: For local dev, use a tunnel (e.g., ngrok) to expose `http://localhost:8000/manager/` and set the webhook to the tunnel URL.

---

## Notion Setup
1. Create a Notion internal integration and copy `NOTION_API_KEY`.
2. Share your databases with the integration.
3. Configure database IDs and group mapping in `skills/utils/group_identify.py`.
4. Available tools:
   - `list_tasks(name)` – list tasks for a group/database
   - `create_new_tasks(name, data)` – create a task via `PersonalTask`
   - `find_task_by_title(name, title)` – query by title
   - `find_task_by_id(id)` – retrieve a page by ID
   - `update_task(task_id, database_name, data)` – update a task

---

## Deployment (Vercel)
This repo includes `vercel.json` for Vercel’s Python runtime:
- Builds `main.py` with `@vercel/python`
- Routes all traffic to `main.py`
- Sets `APP_MODULE=main:app`

Steps:
1. Push to GitHub/GitLab.
2. Import into Vercel.
3. Add env vars in Vercel (same as `.env`).
4. Deploy.

---

## Development
- Lint/format with Ruff:
  - `ruff check .`
  - `ruff format .`
- Pre-commit hooks can be configured if desired (dependency included).

---

## Troubleshooting
- Notion 401/403: Ensure integration is shared with the database and IDs are correct.
- Telegram not replying: Verify webhook URL, server reachability, and `chat_id`.
- Model errors: Confirm model IDs set in env vars exist in your OpenRouter account and you have quota/credits.
- CORS errors: Adjust CORS env vars to match your frontend origins.

---

## License
Add a `LICENSE` file (e.g., MIT).
