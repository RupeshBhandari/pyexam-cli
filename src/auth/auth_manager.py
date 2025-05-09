from src.user.user import User
from .auth import Auth
from src.user.user_manager import UserManager
from src.utils.logger import Logger


class AuthManager:
    def __init__(self) -> None:
        self.logger = Logger()
        self._user_manager: UserManager = UserManager()
        self._current_user: User | None = None
        self._is_authenticated: bool = False
        self.logger.debug("AuthManager initialized")

    def login(self, username: str, password: str) -> bool:
        self.logger.debug(f"Attempting to fetch user: {username}")
        user: User | None = self._user_manager.get_user(username)
        if not user:
            self.logger.warning(f"User not found: {username}")
            return False

        auth = Auth(user, password)
        self.logger.debug(f"{auth._password_hash}")
        if auth.check_password(user._password_hash):
            self._current_user = user
            self._is_authenticated = True
            self.logger.info(f"User authenticated: {username}")
            return True

        self.logger.warning(f"Invalid password for user: {username}")
        return False
