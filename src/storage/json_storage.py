import json
from .base import Storage

class JSONStorage(Storage):
    def __init__(self, filepath: str):
        self.filepath = filepath

    def _read_data(self):
        with open(self.filepath, 'r') as f:
            return json.load(f)

    def _write_data(self, data) -> None:
        with open(self.filepath, 'w') as f:
            json.dump(data, f, indent=4)

    def get_user(self, username: str):
        data = self._read_data()
        return data.get("users", {}).get(username)

    def save_user(self, user_data: dict):
        data = self._read_data()
        users = data.get("users", {})
        users[user_data["username"]] = user_data
        data["users"] = users
        self._write_data(data)

    def get_exam(self, exam_id: str):
        data = self._read_data()
        return data.get("exams", {}).get(exam_id)

    def store_response(self, user_id: str, exam_id: str, response: dict):
        data = self._read_data()
        responses = data.get("responses", {})
        if user_id not in responses:
            responses[user_id] = {}
        responses[user_id][exam_id] = response
        data["responses"] = responses
        self._write_data(data)

