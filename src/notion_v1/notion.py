from notion_client import Client
from src.notion_v1.notion_todo import NotionTodo
from typing import List
import os


class NotionTodoCli(Client):
    def __init__(self, database_id=None, notion_token=None):
        notion_token = notion_token or os.environ['NOTION_TOKEN']
        super().__init__(auth=notion_token)
        self.database_id = database_id or os.environ['DATABASE_ID']
        self.todos = self.get_todos()

    def get_todos(self):
        results = self.databases.query(database_id=self.database_id)['results']
        return [
            NotionTodo(r, self) for r in results
        ]

    def refresh_todos(self):
        self.todos = self.get_todos()
