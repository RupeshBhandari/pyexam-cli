from interface.ui import UI


class UIManager:
    def __init__(self):
        self.ui = UI()

    def show_main_menu(self):
        self.ui.show_main_menu()

    def handle_user_selection(self, selection):
        if selection == "1":
            self.ui.show_login_menu()
        elif selection == "2":
            self.ui.show_register_menu()
        elif selection == "3":
            self.ui.show_exit_message()
        else:
            self.ui.show_error("Invalid selection. Please try again.")

    def show_post_login_menu(self, is_admin):
        self.ui.show_post_login_menu(is_admin)

    def handle_admin_menu_selection(self, selection):
        if selection == "1":
            self.ui.show_user_management_menu()
        elif selection == "2":
            self.ui.show_exam_management_menu()
        elif selection == "3":
            self.ui.show_exit_message()
        else:
            self.ui.show_error("Invalid selection. Please try again.")

    def show_user_profile(self, user):
        self.ui.show_profile(user)
