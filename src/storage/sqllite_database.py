import sqlite3
from .database import Database

class SQLiteDatabase(Database):
    def __init__(self, db_name: str, db_path: str):
        self.db_name = db_name
        self.db_path = db_path
        self.conn = None
        self.cursor = None

    def connect(self):
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()

    def execute(self, query: str, params: tuple = ()):
        self.cursor.execute(query, params)

    def fetchall(self):
        return self.cursor.fetchall()

    def fetchone(self):
        return self.cursor.fetchone()

    def commit(self):
        self.conn.commit()

    def close(self):
        self.cursor.close()
        self.conn.close()
