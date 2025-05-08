class User:
    """Represents a user with username, password hash, and role."""

    VALID_ROLES = {"student", "admin"}

    def __init__(self, username: str, password_hash: str, role: str = "student"):
        self.username = username
        if role not in User.VALID_ROLES:
            raise ValueError("Invalid role")
        self._role = role
        self._password_hash = password_hash

    @property
    def role(self) -> str:
        return self._role

    @role.setter
    def role(self, role: str) -> None:
        if role not in User.VALID_ROLES:
            raise ValueError("Invalid role")
        self._role = role

    def to_dict(self) -> dict:
        return {
            "username": self.username,
            "password_hash": self._password_hash,
            "role": self.role,
        }

    @classmethod
    def from_dict(cls, data: dict):
        """Creates a User instance from a dictionary."""
        # Passsing empty password as we dont want it to be rehashed as its already hashed
        user = cls(data["username"], "", data.get("role", "student"))
        user._password_hash = data["password_hash"]
        return user
