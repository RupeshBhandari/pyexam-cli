from .auth import Auth
from src.user.user_manager import UserManager

class AuthManager:
    def __init__(self):
        self._user_manager: UserManager = UserManager()
        self.auth : Auth = None

    def login(self, username: str, password: str) -> bool:
        user = self._user_manager.get_user(username)
        if user:
            self.auth = Auth(user, password)
            if self.auth.login():
                return True
        return False
    
    def logout(self) -> None:
        self.auth.logout()