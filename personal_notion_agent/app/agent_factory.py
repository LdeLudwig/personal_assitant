from textwrap import dedent
from agno.agent import Agent
from agno.team import Team
from agno.models.google import Gemini

# tools
from skills.tools import (
    create_new_tasks,
    list_tasks,
    find_task_by_title,
    find_task_by_id,
    update_task,
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
            model=Gemini(
                id=self.settings.gemini_pro_model,
                api_key=self.settings.gemini_api_key,
                temperature=self.settings.temperature,
                max_output_tokens=None,
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
        )

        return manager_agent

    def create_telegram_agent(self):
        telegram_agent = Agent(
            name="telegram",
            model=Gemini(
                id=self.settings.gemini_pro_model,
                api_key=self.settings.gemini_api_key,
                temperature=self.settings.temperature,
                max_output_tokens=None,
            ),
            instructions=dedent(telegram_agent_prompt),
            tools=[],
            add_datetime_to_instructions=True,
            debug_mode=True,
        )
        return telegram_agent

    def create_coordinator_agent(self):
        manager_agent = self.create_manager_agent()
        manager_agent.name = "manager"
        manager_agent.role = ()

        telegram_agent = self.create_telegram_agent()
        telegram_agent.name = "telegram"
        telegram_agent.role = ()

        coordinator_agent = Team(
            name="coordinator",
            mode="coordinate",
            model=Gemini(
                id=self.settings.gemini_pro_model,
                api_key=self.settings.gemini_api_key,
                temperature=self.settings.temperature,
                max_output_tokens=None,
            ),
            members=[manager_agent, telegram_agent],
            instructions=dedent(coordinator_agent_prompt),
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
