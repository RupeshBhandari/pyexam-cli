from typing import NoReturn
from src.interface.ui import (
    UI,
    ADMIN_MENU_OPTIONS,
    STUDENT_MENU_OPTIONS,
    ADMIN_MENU_OPTIONS_USER_MANAGEMENT,
    ADMIN_MENU_OPTIONS_EXAM_MANAGEMENT,
)


class UIManager:
    def __init__(self):
        self.ui: UI = UI()

    # ----- Main Flow Management -----
    def start_application(self):
        """Initialize and start the application UI flow"""
        self.ui.show_welcome_banner()
        self.show_main_menu()

    def exit_application(self):
        """Properly exit the application with farewell message"""
        self.ui.show_exit_message()
        exit(0)

    # ----- Menu Display and Navigation -----
    def show_main_menu(self):
        """Display the main application menu"""
        self.ui.show_main_menu()
        return self.ui.ask_input("Select an option")

    def handle_main_menu_selection(self, selection) -> dict[str, str, str] | NoReturn | None:
        """Process user selection from the main menu"""
        if selection == "1":
            return self.show_login_menu()
        elif selection == "2":
            return self.show_register_menu()
        elif selection == "3":
            self.exit_application()
        else:
            self.ui.show_error("Invalid selection. Please try again.")
            return None

    def show_post_login_menu(self, is_admin):
        """Display the appropriate menu based on user role"""
        self.ui.show_post_login_menu(is_admin)
        return self.ui.ask_input("Select an option")

    def handle_post_login_selection(self, selection, is_admin):
        """Process user selection after login based on role"""
        if is_admin:
            return self.handle_admin_menu_selection(selection)
        else:
            return self.handle_student_menu_selection(selection)

    def handle_admin_menu_selection(self, selection):
        """Process admin menu selections"""
        options = list(ADMIN_MENU_OPTIONS.keys())
        if selection == options[0]:  # User Management
            return ""
        elif selection == options[1]:  # Exam Management
            return self.show_exam_management_menu()
        elif selection == options[2]:  # Logout
            return "logout"
        elif selection == options[3]:  # Exit
            self.exit_application()
        else:
            self.ui.show_error("Invalid selection. Please try again.")
            return None

    def handle_student_menu_selection(self, selection):
        """Process student menu selections"""
        options = list(STUDENT_MENU_OPTIONS.keys())
        if selection == options[0]:  # Start Exam
            return "start_exam"
        elif selection == options[1]:  # View Profile
            return "view_profile"
        elif selection == options[2]:  # Logout
            return "logout"
        elif selection == options[3]:  # Exit
            self.exit_application()
        else:
            self.ui.show_error("Invalid selection. Please try again.")
            return None

    # ----- User Management -----
    def show_user_management_menu(self):
        """Display the user management menu for admins"""
        self.ui.console.clear()
        self.ui.print_title("User Management", color="blue")

        table = self.ui.create_menu_table(ADMIN_MENU_OPTIONS_USER_MANAGEMENT)
        self.ui.console.print(table)
        self.ui.print_divider()

        return self.ui.ask_input("Select an option")

    def handle_user_management_selection(self, selection):
        """Process selections from the user management menu"""
        options = list(ADMIN_MENU_OPTIONS_USER_MANAGEMENT.keys())
        if selection == options[0]:  # Register New User
            return "register_user"
        elif selection == options[1]:  # Deregister User
            return "deregister_user"
        elif selection == options[2]:  # View All Users
            return "view_users"
        elif selection == options[3]:  # Update User
            return "update_user"
        elif selection == options[4]:  # View User Profile
            return "view_user_profile"
        elif selection == options[5]:  # Back to Main Menu
            return "admin_menu"
        elif selection == options[6]:  # Exit
            self.exit_application()
        else:
            self.ui.show_error("Invalid selection. Please try again.")
            return None

    # ----- Exam Management -----
    def show_exam_management_menu(self):
        """Display the exam management menu for admins"""
        self.ui.console.clear()
        self.ui.print_title("Exam Management", color="blue")

        table = self.ui.create_menu_table(ADMIN_MENU_OPTIONS_EXAM_MANAGEMENT)
        self.ui.console.print(table)
        self.ui.print_divider()

        return self.ui.ask_input("Select an option")

    def handle_exam_management_selection(self, selection):
        """Process selections from the exam management menu"""
        options = list(ADMIN_MENU_OPTIONS_EXAM_MANAGEMENT.keys())
        if selection == options[0]:  # Add Exam
            return "add_exam"
        elif selection == options[1]:  # View All Exams
            return "view_exams"
        elif selection == options[2]:  # Update Exam
            return "update_exam"
        elif selection == options[3]:  # Delete Exam
            return "delete_exam"
        elif selection == options[4]:  # View Exam Results
            return "view_exam_results"
        elif selection == options[5]:  # Back to Main Menu
            return "admin_menu"
        elif selection == options[6]:  # Exit
            self.exit_application()
        else:
            self.ui.show_error("Invalid selection. Please try again.")
            return None

    # ----- Authentication Flows -----
    def show_login_menu(self) -> dict[str, str]:
        """Display login form and collect credentials"""
        self.ui.show_login_menu()
        username = self.ui.ask_input("Username")
        password = self.ui.ask_password("Password")
        return {"username": username, "password": password, "login": True}

    def show_register_menu(self) -> None | dict[str, str]:
        """Display registration form and collect user details"""
        self.ui.show_register_menu()
        username = self.ui.ask_input("Username")
        password = self.ui.ask_password("Password")
        confirm_password = self.ui.ask_password("Confirm Password")

        if password != confirm_password:
            self.ui.show_error("Passwords do not match!")
            return None

        return {"username": username, "password": password, "login": True}

    # ----- User Profile -----
    def show_user_profile(self, user):
        """Display user profile information"""
        self.ui.show_profile(user)
        self.ui.ask_input("Press Enter to continue...")

    # ----- Exam Interface -----
    def show_exam_interface(self, exam):
        """Initialize and display the exam interface"""
        self.ui.console.clear()
        self.ui.print_title_center(f"Exam: {exam.title}", color="green")
        self.ui.console.print(f"[yellow]Duration:[/yellow] {exam.duration} minutes")
        self.ui.console.print(
            f"[yellow]Total Questions:[/yellow] {len(exam.questions)}"
        )
        self.ui.print_divider()
        self.ui.ask_input("Press Enter to start the exam...")

        return self.handle_exam_questions(exam)

    def handle_exam_questions(self, exam):
        """Process exam questions and user responses"""
        responses = {}

        for i, question in enumerate(exam.questions, 1):
            self.ui.get_mcq_question(
                i, len(exam.questions), question.text, question.choices
            )

            answer = self.ui.ask_input("Your answer (1-4)")

            # Validate input
            if answer.isdigit() and 1 <= int(answer) <= len(question.choices):
                self.ui.print_user_choice(question.choices[int(answer) - 1])
                responses[question.id] = int(answer)
            else:
                self.ui.show_error(
                    "Invalid choice. Please enter a number between 1 and 4."
                )
                i -= 1  # Repeat the same question

        self.ui.show_loading("Calculating results...")
        return responses

    def show_exam_results(self, result_data):
        """Display exam results after completion"""
        self.ui.show_exam_results(
            result_data["exam_name"],
            result_data["correct_count"],
            result_data["total_questions"],
            result_data["earned_points"],
            result_data["total_points"],
        )
        self.ui.ask_input("Press Enter to continue...")

    # ----- Confirmation Dialogs -----
    def confirm_action(self, message):
        """Display a confirmation dialog and return True if confirmed"""
        response = self.ui.ask_input(f"{message} (y/n)")
        return response.lower() in ["y", "yes"]

    # ----- Notifications -----
    def show_success_notification(self, message):
        """Display a success notification and wait for acknowledgment"""
        self.ui.show_success(message)

    def show_error_notification(self, message):
        """Display an error notification and wait for acknowledgment"""
        self.ui.show_error(message)

    def show_info_notification(self, message):
        """Display an informational notification and wait for acknowledgment"""
        self.ui.show_info(message)