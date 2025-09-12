from textwrap import dedent
from agno.agent import Agent
from agno.team import Team
from agno.models.google import Gemini

# tools
from skills.tools import (
    create_new_tasks,
    list_personal_tasks,
    find_personal_task_by_title,
    find_personal_task_by_id,
    update_personal_task,
)

# prompts
from .prompts import (
    notion_agent_prompt,
    responder_agent_prompt,
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
                list_personal_tasks,
                create_new_tasks,
                find_personal_task_by_title,
                find_personal_task_by_id,
                update_personal_task,
            ],
            show_tool_calls=True,
            add_datetime_to_instructions=True,
            debug_mode=True,
        )

        return manager_agent

    def create_responder_agent(self):
        responder_agent = Agent(
            name="telegram",
            model=Gemini(
                id=self.settings.gemini_pro_model,
                api_key=self.settings.gemini_api_key,
                temperature=self.settings.temperature,
                max_output_tokens=None,
            ),
            instructions=dedent(responder_agent_prompt),
            tools=[],
            show_tool_calls=True,
            add_datetime_to_instructions=True,
            debug_mode=True,
        )
        return responder_agent

    def create_coordinator_agent(self):
        manager_agent = self.create_manager_agent()
        manager_agent.name = "manager"
        manager_agent.role = ()

        responder_agent = self.create_responder_agent()
        responder_agent.name = "responder"
        responder_agent.role = ()

        coordinator_agent = Team(
            name="coordinator",
            mode="coordinate",
            model=Gemini(
                id=self.settings.gemini_pro_model,
                api_key=self.settings.gemini_api_key,
                temperature=self.settings.temperature,
                max_output_tokens=None,
            ),
            members=[manager_agent, responder_agent],
            instructions=dedent(coordinator_agent_prompt),
        )

        return coordinator_agent

    def get_agent(self, agent_name: str):
        mapper = {
            "coordinator": self.create_coordinator_agent,
            "manager": self.create_manager_agent,
            "responder": self.create_responder_agent,
        }

        if agent_name not in mapper:
            raise ValueError(f"Unkown Agent - {agent_name}")

        return mapper[agent_name]()
