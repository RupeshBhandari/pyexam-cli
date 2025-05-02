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
    
