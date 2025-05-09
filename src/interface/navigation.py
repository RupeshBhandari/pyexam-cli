from typing import NoReturn
from src.auth.auth_manager import AuthManager
from src.interface.input_handler import InputHandler
from src.exams.exam_manager import ExamManager
from src.storage.database_manager import DatabaseManager
from src.user.user_manager import UserManager
from src.utils.logger import Logger
from src.interface.ui import UI


class Navigation:
    def __init__(self):
        self.logger = Logger()
        self.ui: UI = UI()
        self.input_handler: InputHandler = InputHandler(input_source=input)
        self.database_manager: DatabaseManager = DatabaseManager()
        self.user_manager: UserManager = UserManager(
            ui=self.ui, database=self.database_manager, logger=self.logger
        )
        self.auth_manager: AuthManager = AuthManager(
            ui=self.ui, user_manager=self.user_manager, logger=self.logger
        )
        self.exam_manager: ExamManager = ExamManager(
            ui=self.ui,
            input_handler=self.input_handler,
            user_manager=self.user_manager,
            database_manager=self.database_manager,
            logger=self.logger,
            auth_manager=self.auth_manager,
        )
        self.logger.info("Navigation initialized.")

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
        user = self.auth_manager._current_user
        is_admin = user and getattr(user, "role", None) == "admin"
        self.ui.show_post_login_menu(is_admin=is_admin)
        choice = self.input_handler.get_menu_choice()
        if is_admin:
            match choice:
                case "1":
                    self.add_exam()
                    self.post_login_menu()
                case "2":
                    self.user_manager.create_user()
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
                    self.start_exam()
                    self.post_login_menu()
                case "2":
                    self.show_profile()
                    self.post_login_menu()
                case "3":
                    self.auth_manager.logout()
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

    def add_exam(self):
        """Handler for adding a new exam."""
        user = self.auth_manager.get_current_user()
        if not user:
            self.ui.show_error("You must be logged in to add an exam.")
            return

        # Only admins can add exams
        if user.role != "admin":
            self.ui.show_error("Only administrators can add exams.")
            return

        # Call exam manager's add_exam method
        success = self.exam_manager.add_exam()

    def start_exam(self) -> None:
        """Start taking an exam"""
        # Check if user is logged in
        if not self.auth_manager.get_current_user():
            self.ui.show_error("You must be logged in to take an exam.")
            return

        # Display available exams
        self.exam_manager.list_exams()
        if not self.exam_manager.exams:
            return

        # Get exam selection
        while True:
            exam_id_str = self.input_handler.get_exam_id()
            try:
                exam_id = int(exam_id_str)
                exam = self.exam_manager.get_exam(exam_id)
                if exam:
                    break
                self.ui.show_error(f"Exam with ID {exam_id} not found.")
            except ValueError:
                self.ui.show_error("Please enter a valid exam ID.")

        # Start the exam
        self.exam_manager.take_exam(exam_id)

    def show_profile(self):
        user = self.auth_manager.get_current_user()
        self.ui.show_profile(user)


if __name__ == "__main__":
    n = Navigation()
    n.start()
