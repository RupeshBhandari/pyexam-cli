import sqlite3  
from .base import Storage
import json

class MySQLStorage(Storage):
    def __init__(self, host: str, user: str, password: str, database: str):
        self.conn = sqlite3.connect(database)
        self.cursor = self.conn.cursor()

    def _execute_query(self, query, params=()):
        self.cursor.execute(query, params)
        self.conn.commit()

    def get_user(self, username: str):
        query = "SELECT * FROM users WHERE username = %s"
        self.cursor.execute(query, (username,))
        return self.cursor.fetchone()

    def save_user(self, user_data: dict):
        query = "INSERT INTO users (username, password, email) VALUES (%s, %s, %s)"
        self._execute_query(query, (user_data["username"], user_data["password"], user_data["email"]))

    def get_exam(self, exam_id: str):
        query = "SELECT * FROM exams WHERE id = %s"
        self.cursor.execute(query, (exam_id,))
        return self.cursor.fetchone()

    def store_response(self, user_id: str, exam_id: str, response: dict):
        query = "INSERT INTO responses (user_id, exam_id, response_data) VALUES (%s, %s, %s)"
        self._execute_query(query, (user_id, exam_id, json.dumps(response)))
