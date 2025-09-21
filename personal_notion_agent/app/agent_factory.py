from textwrap import dedent
from agno.agent import Agent
from agno.team import Team

# from agno.models.google import Gemini
from agno.models.openrouter import OpenRouter

# tools
from skills.tools import (
    create_new_tasks,
    list_tasks,
    find_task_by_title,
    find_task_by_id,
    update_task,
    reply,
    get_models,
)

# prompts
from .prompts import (
    notion_agent_prompt,
    telegram_agent_prompt,
    coordinator_agent_prompt,
)


class AgentFactory:
    def __init__(self, settings):
        self.settings = settings

    def create_manager_agent(self):
        manager_agent = Agent(
            name="manager",
            model=OpenRouter(
                id=self.settings.gemini_pro_model_or,
                api_key=self.settings.open_router_api_key,
                temperature=self.settings.temperature,
                max_tokens=None,
            ),
            instructions=dedent(notion_agent_prompt),
            tools=[
                list_tasks,
                create_new_tasks,
                find_task_by_title,
                find_task_by_id,
                update_task,
            ],
            add_datetime_to_instructions=True,
            debug_mode=True,
            show_tool_calls=True,
        )

        return manager_agent

    def create_telegram_agent(self):
        telegram_agent = Agent(
            name="telegram",
            model=OpenRouter(
                id=self.settings.gemini_flash_model_or,
                api_key=self.settings.open_router_api_key,
                temperature=self.settings.temperature,
                max_tokens=None,
            ),
            instructions=dedent(telegram_agent_prompt),
            tools=[reply, get_models],
            add_datetime_to_instructions=True,
            debug_mode=True,
            show_tool_calls=True,
        )
        return telegram_agent

    def create_coordinator_agent(self):
        manager_agent = self.create_manager_agent()
        manager_agent.name = "manager"
        manager_agent.role = "Gerenciar as tarefas e projetos no Notion"

        telegram_agent = self.create_telegram_agent()
        telegram_agent.name = "telegram"
        telegram_agent.role = "Responder ao usuário no Telegram"

        coordinator_agent = Team(
            name="coordinator",
            mode="coordinate",
            model=OpenRouter(
                id=self.settings.gemini_pro_model_or,
                api_key=self.settings.open_router_api_key,
                temperature=self.settings.temperature,
                max_tokens=None,
            ),
            members=[manager_agent, telegram_agent],
            instructions=dedent(coordinator_agent_prompt),
            debug_mode=True,
            show_tool_calls=True,
        )

        return coordinator_agent

    def get_agent(self, agent_name: str):
        mapper = {
            "coordinator": self.create_coordinator_agent,
            "manager": self.create_manager_agent,
            "telegram": self.create_telegram_agent,
        }

        if agent_name not in mapper:
            raise ValueError(f"Unkown Agent - {agent_name}")

        return mapper[agent_name]()
