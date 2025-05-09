from src.user.user import User
from src.auth.auth import Auth
from src.user.user_manager import UserManager
from src.utils.logger import Logger
from src.interface.ui import UI


class AuthManager:
    def __init__(self, ui: UI, user_manager: UserManager, logger: Logger) -> None:
        self.ui: UI = ui
        self._user_manager: UserManager = user_manager
        self.logger: Logger = logger
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
        if auth.check_password(user._password_hash):
            self._current_user = user
            self._is_authenticated = True
            self.logger.info(f"User authenticated: {username}")
            return True

        self.logger.warning(f"Invalid password for user: {username}")
        return False

    def get_current_user(self) -> User | None:
        """Returns the currently logged-in user."""
        return self._current_user

    def logout(self):
        """Logs out the current user."""
        self._current_user = None
        self._is_authenticated = False
        self.logger.info("User logged out")
        self.ui.show_info("Logged out successfully.")
