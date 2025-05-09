from collections.abc import Callable
from .ui import UI


class InputHandler:
    def __init__(self, input_source: Callable[[str], str]) -> None:
        self.input_source = input_source
        self.ui = UI()

    def get_menu_choice(self) -> str:
        return self.ui.ask_input("Choice")

    def get_username(self) -> str:
        return self.ui.ask_input("Username")

    def get_password(self) -> str:
        return self.ui.ask_input("Password")

    def get_email(self) -> str:
        return self.ui.ask_input("Email")

    def get_exam_title(self) -> str:
        return self.ui.ask_input("Exam Title")

    def get_exam_id(self) -> str:
        return self.ui.ask_input("Exam ID")

    def get_exam_duration(self) -> int:
        return int(self.ui.ask_input("Exam Duration (minutes)"))

    def get_exam_questions_count(self) -> int:
        return int(self.ui.ask_input("Number of Questions"))

    def get_exam_date(self) -> str:
        """Get exam date (defaults to today)."""
        from datetime import datetime

        date_input = self.ui.ask_input("Exam Date (YYYY-MM-DD) [Today]")
        if not date_input:
            return datetime.now().strftime("%Y-%m-%d")
        return date_input
