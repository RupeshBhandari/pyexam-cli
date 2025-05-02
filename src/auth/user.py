import hashlib

class User:
    """Represents a user with username, password hash, and role."""
    VALID_ROLES = {'student', 'admin'}

    def __init__(self, username: str, password: str, role: str = 'student'):
        self.username = username
        if role not in User.VALID_ROLES:
            raise ValueError("Invalid role")
        self.role = role
        self.password_hash = self._hash_password(password)

    def _hash_password(self, password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()

    def check_password(self, password: str) -> bool:
        return self.password_hash == self._hash_password(password)
    
    def to_dict(self) -> dict:
        return {
            "username": self.username,
            "password_hash": self.password_hash,
            "role": self.role
        }

    @classmethod
    def from_dict(cls, data: dict):
        """Creates a User instance from a dictionary."""
        # Passsing empty password as we dont want it to be rehashed as its already hashed
        user = cls(data['username'], '', data.get('role', 'student'))
        user.password_hash = data['password_hash']
        return user