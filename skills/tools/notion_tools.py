import os
from dotenv import load_dotenv
from notion_client import (
    Client,
    APIResponseError,
    APIErrorCode,
)
from agno.tools import tool

# Utils
from ..utils.group_identify import group_identify

load_dotenv()

client = Client(auth=os.getenv("NOTION_API_KEY"))


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


@tool(
    name="find_task_by_title",
    description="Busca tarefas no banco pessoal pelo título exato (propriedade 'Name').",
)
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
    name="create_new_tasks",
    description="Cria uma nova tarefa no banco pessoal usando o modelo PersonalTask (name obrigatório; priority, status, relation, start, end opcionais).",
)
def create_new_tasks(name: str, data: dict):
    try:
        group = group_identify(name)

        model = group["model"](data)

        payload = model.to_create_payload(group["database_id"])
        task = client.pages.create(**payload)

        return task

    except APIResponseError as e:
        if e.code == APIErrorCode.ObjectNotFound:
            print(f"Database or related objects not found - {e}")
        else:
            print(f"Error creating Notion page - {e}")


@tool(
    name="update_task",
    description="Atualiza uma tarefa pessoal existente no Notion pelo ID, aplicando os campos fornecidos do modelo PersonalTask.",
)
def update_task(task_id: str, database_name: str, data: dict):
    try:
        group = group_identify(database_name)

        model = group["model"](data)

        payload = model.to_create_payload(group["database_id"])

        task = client.pages.update(task_id, **payload)
        return task
    except APIResponseError as e:
        if e.code == APIErrorCode.ObjectNotFound:
            print(f"Database or related objects not found - {e}")
        else:
            print(f"Error creating Notion page - {e}")
