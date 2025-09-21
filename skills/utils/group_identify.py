import os
import re
from dotenv import load_dotenv
from enum import Enum

# Modelos
from personal_notion_agent.models.personal_task_model import PersonalTask
from personal_notion_agent.models.work_task_model import WorkTask
from personal_notion_agent.models.work_project_model import WorkProject

load_dotenv()

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
    WORK = {
        "database_id": work_tasks_id,
        "name": "trabalho",
        "model": WorkTask,
    }
    PROJECTS = {
        "database_id": work_projects_id,
        "name": "projetos",
        "model": WorkProject,
    }
    MONTHLY_GOALS = {
        "database_id": monthly_goals_id,
        "name": "meta mensal",
        "model": None,
    }
    WEEKLY_GOALS = {
        "database_id": weekly_goals_id,
        "name": "meta semanal",
        "model": None,
    }
    HABITS = {
        "database_id": habit_tracker_id,
        "name": "habit tracker",
        "model": None,
    }


def group_identify(group: str):
    """
    Identifica o grupo de banco de dados com base no nome informado.

    Args:
        group (str): Nome do grupo a ser identificado.

    Returns:
        dict: Dicionário com as informações do grupo identificado.
    """
    # Reconhecimento do grupos por regex
    recognition = {
        GroupCategory.PERSONAL: [r"[Pp]essoal", r"[Pp]essoais", r"[Pp]ersonal"],
        GroupCategory.WORK: [r"[Tt]rabalho"],
        GroupCategory.PROJECTS: [
            r"[Pp]rojeto",
            r"[Pp]rojetos",
            r"[Pp]roject",
            r"[Pp]rojects",
        ],
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
