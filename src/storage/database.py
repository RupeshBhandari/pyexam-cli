from .json_storage import JSONStorage
from .mysql_storage import MySQLStorage
from .base import Storage

class Database:
    def __init__(self, storage: Storage = JSONStorage("./data/data.json")):
        self.storage: JSONStorage = storage

    def register_user(self, user_data: dict):
        self.storage.save_user(user_data)

    def get_user(self, username: str):
        return self.storage.get_user(username)

    def store_exam_response(self, user_id: str, exam_id: str, response: dict):
        self.storage.store_response(user_id, exam_id, response)

if __name__ == "__main__":
    # Example usage
    # Choose the storage type based on your needs
    storage_type = "json"  # or "mysql"
    
    if storage_type == "json":
        storage = JSONStorage("./data/data.json")
    elif storage_type == "mysql":
        storage = MySQLStorage(host="localhost", user="root", password="password", database="exam_db")
    else:
        raise ValueError("Invalid storage type. Choose 'json' or 'mysql'.")

    db = Database(storage)
    # Now you can use db to interact with the database
    # Example: Register a user
    user_data = {
        "username": "test_user",
        "password": "secure_password",
    }
    db.register_user(user_data)