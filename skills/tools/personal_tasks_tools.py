import os
from dotenv import load_dotenv
from notion_client import (
    Client,
    APIResponseError,
    APIErrorCode,
)
from personal_notion_agent.models.personal_task_models import PersonalTask

load_dotenv()


client = Client(auth=os.getenv("NOTION_API_KEY"))
personal_task_database_id = os.getenv("PERSONAL_TASKS_DB_ID")


def list_personal_tasks():
    try:
        tasks = client.databases.query(personal_task_database_id)
        return tasks

    except APIResponseError as e:
        if e.code == APIErrorCode.ObjectNotFound:
            print(f"Pages not found - {e}")
        else:
            print(f"Error - {e}")


def find_personal_task_by_id(id: str):
    try:
        task = client.pages.retrieve(id)
        return task
    except APIResponseError as e:
        if e.code == APIErrorCode.ObjectNotFound:
            print(f"Page not found - {e}")
        else:
            print(f"Error - {e}")


def find_personal_task_by_title(title: str):
    try:
        task = client.databases.query(
            personal_task_database_id,
            filter={"property": "Name", "title": {"equals": title}},
        )
        return task
    except APIResponseError as e:
        if e.code == APIErrorCode.ObjectNotFound:
            print(f"Page not found - {e}")
        else:
            print(f"Error - {e}")


def create_new_tasks(properties: PersonalTask):
    """Create a new page in the Personal Tasks database using the PersonalTask model."""
    try:
        payload = properties.to_create_payload(personal_task_database_id)
        task = client.pages.create(**payload)

        return task

    except APIResponseError as e:
        if e.code == APIErrorCode.ObjectNotFound:
            print(f"Database or related objects not found - {e}")
        else:
            print(f"Error creating Notion page - {e}")


def update_personal_task(task_id: str, properties: PersonalTask):
    try:
        task = client.pages.update(
            task_id, **properties.to_create_payload(personal_task_database_id)
        )
        return task
    except APIResponseError as e:
        if e.code == APIErrorCode.ObjectNotFound:
            print(f"Database or related objects not found - {e}")
        else:
            print(f"Error creating Notion page - {e}")
