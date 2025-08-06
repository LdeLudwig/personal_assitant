import os
import json
from notion_client import Client

class NotionManager:
    def __init__(self):
        self.client = Client(auth=os.getenv("NOTION_API_KEY"))
        self.work_tasks_DB_ID = os.getenv("WORK_TASKS_DB_ID")

    def get_database(self, database_id):
        try:
            database = self.client.databases.query(database_id)
            
            return json.dumps(database, indent=2)    
        
        except Exception as e:
            print(f"Error getting database: {e}")

    
    
if __name__ == "__main__":
    notion_manager = NotionManager()
    database = notion_manager.get_database(notion_manager.work_tasks_DB_ID)
    print(database)
    