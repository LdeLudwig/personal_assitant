import os
from notion_client import (
    Client,
    APIResponseError,
    APIErrorCode,
)
from personal_notion_agent.models.personal_task_model import PersonalTask

client = Client(auth=os.getenv("NOTION_API_KEY"))
personal_task_database_id = os.getenv("PERSONAL_TASKS_DB_ID")


def list_personal_tasks(filter: bool):
    try:
        tasks = client.databases.query(personal_task_database_id)    
        return tasks
            
    except APIResponseError as e:
        if e.code == APIErrorCode.ObjectNotFound:
            print(f"Pages not found - {e}")
        else:
            print(f"Error - {e}")
            
def create_new_tasks(properties: PersonalTask):
    """Create a new page in the Personal Tasks database using the PersonalTask model."""
    try:
        payload = properties.to_create_payload(personal_task_database_id)
        page = client.pages.create(**payload)
        
        return page
        
    except APIResponseError as e:
        if e.code == APIErrorCode.ObjectNotFound:
            print(f"Database or related objects not found - {e}")
        else:
            print(f"Error creating Notion page - {e}")
        raise
    except ValueError as e:
        # Raised by model validation/conversion (e.g., end < start)
        print(f"Invalid task data: {e}")
        raise