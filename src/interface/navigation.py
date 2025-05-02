from typing import NoReturn
from .input_handler import InputHandler
from .ui import UI
from src.auth import User, Auth

class Navigation:
    def __init__(self):  
        self.ui: UI  = UI()
        self.input_handler: InputHandler = InputHandler(input_source=input)
        self.user: User = User(username='', password='')
        self.auth: Auth = Auth()            

    def start(self):
        self.ui.show_main_menu()
        choice = self.input_handler.get_menu_choice()
        match choice:
            case '1':
                self.login()
            case '2':
                self.register()
            case '3':
                self.exit()
            case _:
                self.ui.show_error("Invalid choice. Please try again.")
                self.start()

    def exit(self) -> NoReturn:
        self.ui.show_exit_message()
        quit()

    def login(self) -> None:
        self.ui.show_login_menu()
        username = self.input_handler.get_username()
        password = self.input_handler.get_password()
        if self.auth.login(username, password):      
            self.ui.show_login_success()
            self.start_exam()
        else:
            self.ui.show_login_failure()
            self.start()                        

    def register(self) -> None:
        self.ui.show_register_menu()
        username = self.input_handler.get_username()
        password = self.input_handler.get_password()
        if self.auth.register(username, password):
            self.ui.show_registration_success()
            self.start()  
        else:
            self.ui.show_registration_failure()
            self.start()  

    def start_exam(self) -> None:
        self.ui.show_info("Starting the exam...")
        # Here you would implement the logic to start the exam, such as loading questions, etc.

if __name__ == '__main__':
    n = Navigation()
    n.start()