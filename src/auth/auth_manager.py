from src.user.user import User
from src.auth.auth import Auth
from src.user.user_manager import UserManager
from src.utils.logger import Logger
from src.interface.ui_manager import UIManager


class AuthManager:
    def __init__(self, ui_manager: UIManager, user_manager: UserManager, logger: Logger) -> None:
        self._ui_manager: UIManager = ui_manager
        self._user_manager: UserManager = user_manager
        self._logger: Logger = logger
        self._current_user: User | None = None
        self._is_authenticated: bool = False
        self._logger.debug("AuthManager initialized")

    def login(self, username: str, password: str) -> bool:
        self._logger.debug(f"Attempting to fetch user: {username}")
        user: User | None = self._user_manager.get_user(username)
        if not user:
            self._logger.warning(f"User not found: {username}")
            return False

        auth = Auth(user, password)
        if auth.check_password(user._password_hash):
            self._current_user = user
            self._is_authenticated = True
            self._logger.info(f"User authenticated: {username}")
            return True

        self._logger.warning(f"Invalid password for user: {username}")
        return False

    def get_current_user(self) -> User | None:
        """Returns the currently logged-in user."""
        return self._current_user

    def logout(self):
        """Logs out the current user."""
        self._current_user = None
        self._is_authenticated = False
        self._logger.info("User logged out")
        self.ui_manager.show_success_notification("You have logged out.")
