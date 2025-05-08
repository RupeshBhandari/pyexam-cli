from typing import NoReturn
from src.auth.auth_manager import AuthManager
from .input_handler import InputHandler
from .ui import UI
from src.exams import Exam
from src.storage.database_manager import DatabaseManager
from src.user.user_manager import UserManager

class Navigation:
    def __init__(self):
        self.ui: UI = UI()
        self.input_handler: InputHandler = InputHandler(input_source=input)
        self.user_manager: UserManager = UserManager()
        self.database_manager: DatabaseManager = DatabaseManager()
        self.auth_manager: AuthManager = AuthManager()

    def start(self):
        # Show main menu before login
        self.ui.show_main_menu()
        choice = self.input_handler.get_menu_choice()
        match choice:
            case "1":
                if self.login():
                    self.ui.show_login_success()
                    self.post_login_menu()
                else:
                    self.ui.show_login_failure()
                    self.start()
            case "2":
                self.register()
                self.start()
            case "3":
                self.exit()
            case _:
                self.ui.show_error("Invalid choice. Please try again.")
                self.start()

    def post_login_menu(self):
        user = self.auth.get_current_user()
        is_admin = user and getattr(user, "role", None) == "admin"
        self.ui.show_post_login_menu(is_admin=is_admin)
        choice = self.input_handler.get_menu_choice()
        if is_admin:
            match choice:
                case "1":
                    self.add_exam()
                case "2":
                    self.show_profile()
                    self.post_login_menu()
                case "3":
                    self.register()
                    self.post_login_menu()
                case "4":
                    self.exit()
                case _:
                    self.ui.show_error("Invalid choice. Please try again.")
                    self.post_login_menu()
        else:
            match choice:
                case "1":
                    self.add_exam()
                case "2":
                    self.show_profile()
                    self.post_login_menu()
                case "3":
                    self.auth.logout()
                    self.ui.show_info("Logged out successfully.")
                    self.start()
                case "4":
                    self.exit()
                case _:
                    self.ui.show_error("Invalid choice. Please try again.")
                    self.post_login_menu()

    def exit(self) -> NoReturn:
        self.ui.show_exit_message()
        quit()

    def login(self) -> None:
        self.ui.show_login_menu()
        username = self.input_handler.get_username()
        password = self.input_handler.get_password()
        return self.auth_manager.login(username, password)

    def register(self) -> None:
        """Handles user registration."""

        self.ui.show_register_menu()
        username = self.input_handler.get_username()
        password = self.input_handler.get_password()
        if not self.user_manager.register(username, password):
            self.ui.show_error("Registration failed! Please try again.")
            self.ui.print_divider()
            return

        self.ui.show_registration_success()
        self.start()

    def start_exam(self) -> None:
        self.ui.show_info("Starting the exam...")
        # Here you would implement the logic to start the exam, such as loading questions, etc.

    def show_profile(self):
        user = self.auth.get_current_user()
        self.ui.show_profile(user)

    def add_exam(self):
        self.ui.print_title("Add New Exam", color="green")
        exam_id = self.input_handler.get_exam_id()
        title = self.input_handler.get_exam_title()
        duration = self.input_handler.get_exam_duration()
        questions_count = self.input_handler.get_exam_questions_count()
        created_by = (
            self.auth.get_current_user().username
            if self.auth.get_current_user()
            else "admin"
        )
        exam_data: Exam = self.exam.from_dict(
            {
                "exam_id": exam_id,
                "name": title,
                "date": self.input_handler.get_exam_date(),
                "duration": duration,
                "questions_count": questions_count,
                "created_by": created_by,
            }
        )
        exam_data.save_exam()
        self.ui.show_success("Exam added successfully!")


if __name__ == "__main__":
    n = Navigation()
    n.start()
