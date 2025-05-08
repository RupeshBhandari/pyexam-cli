import json
from .sqllite_database import SQLiteDatabase

PATH = "config/database.json"


class DatabaseManager:
    def __init__(self):
        self.database_name = self.retrieve_database_settings("db_name")
        self.database_path = self.retrieve_database_settings("path")
        self.db = SQLiteDatabase(self.database_name, self.database_path)
        self.db.connect()

    def __enter__(self):
        self.db.connect()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is None:
            self.db.commit()
        else:
            print("An error occurred:", exc_value)
        self.db.close()

    def execute(self, query: str, params: tuple = ()):
        self.db.execute(query, params)

    def fetchall(self):
        return self.db.fetchall()

    def fetchone(self):
        return self.db.fetchone()

    @staticmethod
    def retrieve_database_settings(key: str, file_path: str = PATH) -> str:
        with open(file_path, "r") as file:
            data = json.load(file)
            data = data["DATABASE"][key]
        return data
