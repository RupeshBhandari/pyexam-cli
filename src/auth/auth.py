from src.user.user import User
import hashlib
class Auth:
    def __init__(self, user: User, password: str) -> None:
        self.user: User = user
        self._password_hash: str = self._hash_password(password)
        self.current_user: User | None = None
        self._is_authenticated: bool = False

    def login(self) -> bool:
        if not self.check_password(self.user._password_hash):
            return False
        self.current_user = self.user
        self._is_authenticated = True
        return True

    def logout(self) -> None:
        self.current_user = None
        self._is_authenticated = False
    
    def check_password(self, password: str) -> bool:
        return self._password_hash == self._hash_password(password)
    
    @staticmethod
    def _hash_password(password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()