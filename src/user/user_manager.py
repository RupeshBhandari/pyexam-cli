from src.user.user import User
from src.storage.database_manager import DatabaseManager
from src.interface.ui_manager import UIManager
from src.utils.logger import Logger
import sqlite3


class UserManager:
    def __init__(
        self, ui_manager: UIManager, database: DatabaseManager, logger: Logger
    ) -> None:
        self.database: DatabaseManager = database
        self.ui_manager: UIManager = ui_manager
        self._logger: Logger = logger

    def create_user(self, username: str, password: str, role: str) -> User:
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
        """Fetches a user from the database by username."""
        with self.database as db:
            db.execute(
                "SELECT username, password, role FROM users WHERE username = ?",
                (username,),
            )
            row = db.fetchone()
        if row:
            return User(row[0], row[1], row[2])
        return None

    def register(self, username: str, password: str, role: str = "student") -> bool:
        if self.database.get_user(username):
            self.ui.show_error("User already exists!")
            self.ui.print_divider()
            return False  # User already exists
        user = User(username, password, role)
        self.create_user(user.to_dict())
        return True

    def update_user(self, username, password=None, role=None) -> bool:
        """Updates user information."""
        with self.database as db:
            if password:
                db.execute(
                    "UPDATE users SET password = ? WHERE username = ?",
                    (password, username),
                )
            if role:
                db.execute(
                    "UPDATE users SET role = ? WHERE username = ?",
                    (role, username),
                )
        return True

    def delete_user(self, username) -> bool:
        """Deletes a user from the database."""
        with self.database as db:
            db.execute(
                "DELETE FROM users WHERE username = ?",
                (username,),
            )
        return True
