import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import unittest
from unittest.mock import MagicMock, patch
from src.interface.navigation import Navigation


class TestNavigation(unittest.TestCase):
    def setUp(self):
        self.navigation = Navigation()
        self.navigation.ui = MagicMock()
        self.navigation.input_handler = MagicMock()
        self.navigation.auth = MagicMock()

    def test_exit_calls_show_exit_message_and_quit(self):
        with patch("builtins.quit") as mock_quit:
            self.navigation.exit()
            self.navigation.ui.show_exit_message.assert_called_once()
            mock_quit.assert_called_once()

    def test_login_success(self):
        self.navigation.input_handler.get_username.return_value = "user"
        self.navigation.input_handler.get_password.return_value = "pass"
        self.navigation.auth.login.return_value = True
        self.navigation.login()
        self.navigation.ui.show_login_success.assert_called_once()
        self.navigation.ui.show_login_failure.assert_not_called()

    def test_login_failure(self):
        self.navigation.input_handler.get_username.return_value = "user"
        self.navigation.input_handler.get_password.return_value = "wrong"
        self.navigation.auth.login.return_value = False
        with patch.object(self.navigation, "start") as mock_start:
            self.navigation.login()
            self.navigation.ui.show_login_failure.assert_called_once()
            mock_start.assert_called_once()

    def test_register_success(self):
        self.navigation.input_handler.get_username.return_value = "newuser"
        self.navigation.input_handler.get_password.return_value = "newpass"
        self.navigation.auth.register.return_value = True
        with patch.object(self.navigation, "start") as mock_start:
            self.navigation.register()
            self.navigation.ui.show_registration_success.assert_called_once()
            mock_start.assert_called_once()

    def test_register_failure(self):
        self.navigation.input_handler.get_username.return_value = "newuser"
        self.navigation.input_handler.get_password.return_value = "newpass"
        self.navigation.auth.register.return_value = False
        with patch.object(self.navigation, "start") as mock_start:
            self.navigation.register()
            self.navigation.ui.show_registration_failure.assert_called_once()
            mock_start.assert_called_once()

    def test_start_exam_calls_show_info(self):
        self.navigation.ui.show_info = MagicMock()
        self.navigation.start_exam()
        self.navigation.ui.show_info.assert_called_once_with("Starting the exam...")

    def test_start_menu_choice_1(self):
        self.navigation.input_handler.get_menu_choice.return_value = "1"
        self.navigation.login = MagicMock()
        self.navigation.start_exam = MagicMock()
        self.navigation.start()
        self.navigation.login.assert_called_once()
        self.navigation.start_exam.assert_called_once()

    def test_start_menu_choice_2(self):
        self.navigation.input_handler.get_menu_choice.return_value = "2"
        self.navigation.register = MagicMock()
        self.navigation.start()
        self.navigation.register.assert_called_once()

    def test_start_menu_choice_3(self):
        self.navigation.input_handler.get_menu_choice.return_value = "3"
        self.navigation.exit = MagicMock()
        self.navigation.start()
        self.navigation.exit.assert_called_once()

    def test_start_menu_invalid_choice(self):
        self.navigation.input_handler.get_menu_choice.side_effect = ["invalid", "3"]
        self.navigation.exit = MagicMock()
        self.navigation.ui.show_error = MagicMock()
        self.navigation.start()
        self.navigation.ui.show_error.assert_called_with(
            "Invalid choice. Please try again."
        )
        self.navigation.exit.assert_called_once()


if __name__ == "__main__":
    unittest.main()
