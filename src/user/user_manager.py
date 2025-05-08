import sqlite3
from .user import User
from src.storage.database_manager import DatabaseManager


class UserManager:
    def __init__(self) -> None:
        self.database = DatabaseManager()

    def create_user(self, username, password, role) -> User:
        try:
            with self.database as db:
                db.execute(
                    "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                    (username, password, role),
                )
            return User(username, password, role)
        except sqlite3.IntegrityError:
            raise ValueError("User already exists")

    def get_user(self, username) -> User | None:
        cursor = self.database.execute(
            "SELECT username, password, is_active FROM users WHERE username = ?",
            (username,),
        )
        row = cursor.fetchone()
        if row:
            return User(row[0], row[1], bool(row[2]))
        return None
    
    def register(self, username: str, password: str, role: str = 'student') -> bool:
        if self.database.get_user(username):
            self.ui.show_error("User already exists!")
            self.ui.print_divider()
            return False  # User already exists
        user = User(username, password, role)
        self.database.register_user(user.to_dict())
        return True

    