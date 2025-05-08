from src.storage.database import Database
from src.auth.user import User
from src.interface.ui import UI

class Auth:
    def __init__(self):
        self.database = Database()
        self.ui = UI()
        self.current_user: User | None = None

    def register(self, username: str, password: str, role: str = 'student') -> bool:
        if self.database.get_user(username):
            self.ui.show_error("User already exists!")
            self.ui.print_divider()
            return False  # User already exists
        user = User(username, password, role)
        self.database.register_user(user.to_dict())
        return True

    def login(self, username: str, password: str) -> bool:
        user_data = self.database.get_user(username)
        user: User = User.from_dict(user_data)
        print(user_data)
        if not user.check_password(password):
            return False
        self.current_user = user
        return True
    
    def check_password(self, password: str) -> bool:
        if self.current_user:
            return self.current_user.check_password(password)
        return False

    def logout(self) -> None:
        self.current_user = None

    def is_authenticated(self) -> bool:
        return self.current_user is not None
    
    def get_current_user(self) -> User | None:
        return self.current_user