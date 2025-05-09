from typing import NoReturn, Optional, Dict, Any
from src.auth.auth_manager import AuthManager
from src.interface.input_handler import InputHandler
from src.exams.exam_manager import ExamManager
from src.storage.database_manager import DatabaseManager
from src.user.user_manager import UserManager
from src.utils.logger import Logger
from src.interface.ui_manager import UIManager


class Navigation:
    def __init__(self) -> None:
        self.logger = Logger()
        self.ui_manager = UIManager()
        self.input_handler: InputHandler = InputHandler(input_source=input)
        self.database_manager: DatabaseManager = DatabaseManager()
        self.user_manager: UserManager = UserManager(
            ui_manager=self.ui_manager,
            database=self.database_manager,
            logger=self.logger,
        )
        self.auth_manager: AuthManager = AuthManager(
            ui_manager=self.ui_manager,
            user_manager=self.user_manager,
            logger=self.logger,
        )
        self.exam_manager: ExamManager = ExamManager(
            ui_manager=self.ui_manager,
            input_handler=self.input_handler,
            user_manager=self.user_manager,
            database_manager=self.database_manager,
            logger=self.logger,
            auth_manager=self.auth_manager,
        )
        self.logger.info("Navigation initialized.")

    def start(self) -> None:
        """Main application flow starting point"""
        while True:
            selection = self.ui_manager.show_main_menu()
            result: dict[str, str, str] | None = self.ui_manager.handle_main_menu_selection(selection)
            print(result)
            if result['login']:
                # Handle login
                if self.process_login(result["username"], result["password"]):
                    self.post_login_flow()
            else:
                # Handle registration
                self.process_registration(result["username"], result["password"])

            # If we reach here, we're back at the main menu or there was an error

    def process_login(self, username: str, password: str) -> bool:
        """Process login credentials and show appropriate feedback"""
        success = self.auth_manager.login(username, password)
        if success:
            self.ui_manager.show_success_notification("Login successful! Welcome back.")
            return True
        else:
            self.ui_manager.show_error_notification(
                "Login failed. Please check your credentials."
            )
            return False

    def process_registration(self, username: str, password: str) -> bool:
        """Process registration information and show appropriate feedback"""
        success = self.user_manager.register(username, password)
        if success:
            self.ui_manager.show_success_notification(
                "Registration successful! You can now log in."
            )
            return True
        else:
            self.ui_manager.show_error_notification(
                "Registration failed. Please try again."
            )
            return False

    def post_login_flow(self) -> None:
        """Handle navigation after successful login"""
        user = self.auth_manager.get_current_user()
        if not user:
            self.logger.error("No user found after login")
            return

        is_admin = user.role == "admin"

        while True:
            selection = self.ui_manager.show_post_login_menu(is_admin)
            if is_admin:
                match selection if is_admin else selection:
                    case "1":
                        self.ui_manager.show_exam_management_menu()
                    case "2":
                        self.ui_manager.show_user_management_menu()
                    case "3":
                        self.auth_manager.logout()
                        return
                    case "4":
                        self.ui_manager.exit_application()
                        return
                    case _:
                        self.ui_manager.show_error_notification(
                            "Invalid selection. Please try again."
                        )
            else:
                match selection:
                    case "1":
                        self.start_exam()
                    case "2":
                        self.show_profile()
                    case "3":
                        self.auth_manager.logout()
                        return
                    case "4":
                        self.ui_manager.exit_application()
                        return
                    case _:
                        self.ui_manager.show_error_notification(
                            "Invalid selection. Please try again."
                        )

    def exit(self) -> NoReturn:
        """Exit the application gracefully"""
        self.ui_manager.exit_application()

    # ----- Exam Management Functions -----

    def add_exam(self) -> None:
        """Handle adding a new exam"""
        user = self.auth_manager.get_current_user()

        if not user or user.role != "admin":
            self.ui_manager.show_error_notification(
                "Only administrators can add exams."
            )
            return

        # Call exam manager's add_exam method and show appropriate feedback
        success = self.exam_manager.add_exam()
        if success:
            self.ui_manager.show_success_notification("Exam added successfully!")
        else:
            self.ui_manager.show_error_notification("Failed to add exam.")

    def view_all_exams(self) -> None:
        """Display all available exams"""
        exams = self.exam_manager.get_all_exams()
        # Implement exam list display logic here
        # ...

    def update_exam(self) -> None:
        """Handle updating an existing exam"""
        # Implement exam update logic here
        # ...
        pass

    def delete_exam(self) -> None:
        """Handle deleting an exam"""
        # Implement exam deletion logic here
        # ...
        pass

    def view_exam_results(self) -> None:
        """View results of completed exams"""
        # Implement exam results viewing logic here
        # ...
        pass

    def start_exam(self) -> None:
        """Start taking an exam"""
        # Check if user is logged in
        if not self.auth_manager.get_current_user():
            self.ui_manager.show_error_notification(
                "You must be logged in to take an exam."
            )
            return

        # Display available exams
        exams = self.exam_manager.list_exams()
        if not exams:
            self.ui_manager.show_exam_interface("No exams available at this time.")
            return

        # Get exam selection
        while True:
            exam_id_str = self.input_handler.get_exam_id()
            try:
                exam_id = int(exam_id_str)
                exam = self.exam_manager.get_exam(exam_id)
                if exam:
                    break
                self.ui_manager.show_error(f"Exam with ID {exam_id} not found.")
            except ValueError:
                self.ui_manager.show_error("Please enter a valid exam ID.")

        # Start the exam
        result_data = self.exam_manager.take_exam(exam_id)
        if result_data:
            self.ui_manager.show_exam_results(result_data)

    # ----- User Management Functions -----

    def register_admin_user(self) -> None:
        """Register a new user as an admin"""
        # Similar to register but with admin privileges
        result = self.ui_manager.show_register_menu()
        if result:
            success = self.user_manager.register(
                result["username"],
                result["password"],
                role="admin",  # Specify admin role
            )
            if success:
                self.ui_manager.show_success_notification(
                    "Admin user registered successfully!"
                )
            else:
                self.ui_manager.show_error_notification(
                    "Failed to register admin user."
                )

    def view_all_users(self) -> None:
        """Display all registered users"""
        users = self.user_manager.get_all_users()
        # Implement user list display logic here
        # ...

    def update_user(self) -> None:
        """Update an existing user's information"""
        # Implement user update logic here
        # ...
        pass

    def deregister_user(self) -> None:
        """Remove a user from the system"""
        # Implement user deletion logic here
        # ...
        pass

    def view_user_profile(self) -> None:
        """View a specific user's profile"""
        # Ask for username
        username = self.ui_manager.ask_input("Enter username to view")
        user = self.user_manager.get_user_by_username(username)
        if user:
            self.ui_manager.show_user_profile(user)
        else:
            self.ui_manager.show_error_notification(f"User '{username}' not found.")

    def show_profile(self) -> None:
        """Show the current user's profile"""
        user = self.auth_manager.get_current_user()
        self.ui_manager.show_user_profile(user)


if __name__ == "__main__":
    n = Navigation()
    n.start()
