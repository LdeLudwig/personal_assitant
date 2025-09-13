import os
import re
import json
from dotenv import load_dotenv
from enum import Enum
from notion_client import (
    Client,
    APIResponseError,
    APIErrorCode,
)
from agno.tools import tool
import sys
from pathlib import Path

# Permite rodar diretamente: `python skills/tools/notion_tools.py`
# Garante que o diretório raiz do projeto esteja no sys.path
if __name__ == "__main__" or __package__ in (None, ""):
    project_root = Path(__file__).resolve().parents[2]
    project_root_str = str(project_root)
    if project_root_str not in sys.path:
        sys.path.insert(0, project_root_str)

from personal_notion_agent.models.personal_task_models import PersonalTask
from personal_notion_agent.models.work_task_model import WorkTask


load_dotenv()

client = Client(auth=os.getenv("NOTION_API_KEY"))
personal_tasks_id = os.getenv("PERSONAL_TASKS_DB_ID")
work_tasks_id = os.getenv("WORK_TASKS_DB_ID")
work_projects_id = os.getenv("PROJECTS_DB_ID")
monthly_goals_id = os.getenv("MONTHLY_GOALS_ID")
weekly_goals_id = os.getenv("WEEKLY_GOALS_ID")
habit_tracker_id = os.getenv("HABIT_TRACKER_ID")


class GroupCategory(Enum):
    PERSONAL = {
        "database_id": personal_tasks_id,
        "name": "pessoal",
        "model": PersonalTask,
    }
    WORK = {"database_id": work_tasks_id, "name": "trabalho", "model": WorkTask}
    PROJECTS = {"database_id": work_projects_id, "name": "projetos", "model": ""}


def group_identify(group: str):
    # Reconhecimento do grupos por regex
    recognition = {
        GroupCategory.PERSONAL: [r"[Pp]essoal", r"[Pp]essoais", r"[Pp]ersonal"],
        GroupCategory.WORK: [r"[Tt]rabalho"],
        GroupCategory.PROJECTS: [r"[Pp]rojeto", r"[Pp]rojetos", r"[Pp]roject"],
    }

    try:
        for category, patterns in recognition.items():
            for pattern in patterns:
                if re.search(pattern, group, re.IGNORECASE):
                    return category.value

        # Se não encontrou correspondência, retorna pessoal como padrão
        print(f"Grupo '{group}' não identificado, usando 'pessoal' como padrão")
        return GroupCategory.PERSONAL.value

    except Exception as e:
        print(f"Erro ao identificar grupo - {e}")
        return GroupCategory.PERSONAL.value


@tool(
    name="find_task_by_id",
    description="Busca uma página de tarefa específica no Notion pelo ID da página.",
)
def find_task_by_id(id: str):
    try:
        task = client.pages.retrieve(id)
        return task
    except APIResponseError as e:
        if e.code == APIErrorCode.ObjectNotFound:
            print(f"Page not found - {e}")
        else:
            print(f"Error - {e}")


@tool(
    name="list_tasks",
    description="Lista páginas de tarefas em um banco do Notion com base no grupo identificado a partir do nome informado (ex.: 'pessoal', 'trabalho', 'projetos').",
)
def list_tasks(name: str):
    try:
        group = group_identify(name)

        if group:
            tasks = client.databases.query(group["database_id"])
            return tasks
        else:
            raise print(
                f"Grupo '{name}' não identificado, usando 'pessoal' como padrão"
            )

    except APIResponseError as e:
        if e.code == APIErrorCode.ObjectNotFound:
            print(f"Pages not found - {e}")
        else:
            print(f"Error - {e}")


# @tool(name="find_personal_task_by_title", description="Busca tarefas no banco pessoal pelo título exato (propriedade 'Name').")
def find_task_by_title(name: str, title: str):
    try:
        group = group_identify(name)

        task = client.databases.query(
            group["database_id"],
            filter={"property": "Name", "title": {"equals": title}},
        )
        return task
    except APIResponseError as e:
        if e.code == APIErrorCode.ObjectNotFound:
            print(f"Page not found - {e}")
        else:
            print(f"Error - {e}")


@tool(
    name="create_new_personal_tasks",
    description="Cria uma nova tarefa no banco pessoal usando o modelo PersonalTask (name obrigatório; priority, status, relation, start, end opcionais).",
)
def create_new_tasks(name: str):
    try:
        group = group_identify(name)
        payload = group["model"].to_create_payload(group["database_id"])
        task = client.pages.create(**payload)

        return task

    except APIResponseError as e:
        if e.code == APIErrorCode.ObjectNotFound:
            print(f"Database or related objects not found - {e}")
        else:
            print(f"Error creating Notion page - {e}")


@tool(
    name="update_personal_task",
    description="Atualiza uma tarefa pessoal existente no Notion pelo ID, aplicando os campos fornecidos do modelo PersonalTask.",
)
def update_task(task_id: str, properties: PersonalTask):
    try:
        task = client.pages.update(
            task_id, **properties.to_create_payload(personal_tasks_id)
        )
        return task
    except APIResponseError as e:
        if e.code == APIErrorCode.ObjectNotFound:
            print(f"Database or related objects not found - {e}")
        else:
            print(f"Error creating Notion page - {e}")


if __name__ == "__main__":
    tasks = find_task_by_title("projeto", "DanCafé")

    print(json.dumps(tasks, indent=2))
