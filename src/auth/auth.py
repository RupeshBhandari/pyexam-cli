from src.user.user import User
import hashlib

class Auth:
    def __init__(self, user: User, password: str) -> None:
        self.user: User = user
        self._password_hash: str = self._hash_password(password)

    def check_password(self, stored_hash: str) -> bool:
        return self._password_hash == stored_hash
    
    @staticmethod
    def _hash_password(password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()