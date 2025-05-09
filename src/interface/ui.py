from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.text import Text
from rich import box
from rich.align import Align

MAIN_MENU_OPTIONS = {
    "1": "Login",
    "2": "Register",
    "3": "Exit",
}

STUDENT_MENU_OPTIONS = {
    "1": "Start Exam",
    "2": "View Profile",
    "3": "Logout",
    "4": "Exit",
}

ADMIN_MENU_OPTIONS = {
    "1": "Add Exam",
    "2": "Register New User",
    "3": "Deregister User",
    "4": "View All Users",
    "5": "Logout",
    "6": "Exit",
}


class UI:
    _isinstance = None

    def __new__(cls, *args, **kwargs):
        if not cls._isinstance:
            cls._isinstance = super(UI, cls).__new__(cls)
        return cls._isinstance
    
    def __init__(self) -> None:
        self.console = Console()

    # ----- Section Headers -----
    def print_title(self, title: str, color="cyan") -> None:
        panel = Panel(title, style=f"bold {color}", expand=False, box=box.ROUNDED)
        self.console.print(panel)

    def print_title_center(self, title: str, color="cyan") -> None:
        panel = Panel(
            Align.center(f"[bold]{title}[/bold]"),
            style=f"bold {color}",
            expand=False,
            box=box.ROUNDED,
        )
        self.console.print(panel)

    def print_divider(self) -> None:
        self.console.rule(style="dim")

    # ----- Input Prompts -----
    def ask_input(self, message: str) -> str:
        return Prompt.ask(f"[bold magenta]{message}[/bold magenta]")

    # ----- Standardized Messages -----
    def show_success(self, message: str) -> None:
        self.console.print(f"✅ [green]{message}[/green]")

    def show_error(self, message: str) -> None:
        self.console.print(f"❌ [bold red]{message}[/bold red]")

    def show_info(self, message: str) -> None:
        self.console.print(f"ℹ️ [yellow]{message}[/yellow]")

    # ----- Menu Displays -----
    def show_main_menu(self) -> None:
        self.print_title("Welcome to PyExam!", color="blue")
        for key, value in MAIN_MENU_OPTIONS.items():
            self.console.print(f"[{key}] {value}")

    def show_post_login_menu(self, is_admin=False) -> None:
        self.print_title("Main Menu", color="blue")
        if is_admin:
            for key, value in ADMIN_MENU_OPTIONS.items():
                self.console.print(f"[{key}] {value}")
        else:
            for key, value in STUDENT_MENU_OPTIONS.items():
                self.console.print(f"[{key}] {value}")

    def show_exit_message(self) -> None:
        self.print_title("Thank You for Using PyExam!", color="blue")
        self.console.print("[bold red]Exiting the application. Goodbye![/bold red]")
        self.print_divider()  # Added print_divider() for consistency

    # ----- Login and Registration -----
    def show_login_menu(self) -> None:
        self.print_title("Login Menu", color="green")

    def show_login_success(self) -> None:
        self.show_success("Login successful!")

    def show_login_failure(self) -> None:
        self.show_error("Login failed! Please check your username and password.")

    def show_register_menu(self) -> None:
        self.print_title("Register Menu", color="green")

    def show_registration_success(self) -> None:
        self.show_success("Registration successful! You can now log in.")

    def show_registration_failure(self) -> None:
        self.show_error("Registration failed! Please try again.")

    # ----- Question Presentation -----
    def get_mcq_question(
        self, question_no: int, total_questions: int, question: str, choices: list
    ) -> None:
        self.console.rule(f"[bold blue]Question {question_no} of {total_questions}")
        self.console.print(f"[bold]{question}[/bold]")
        for index, choice in enumerate(choices, start=1):
            self.console.print(f"  {index}. {choice}")
        self.print_divider()

    def print_user_choice(self, choice: str) -> None:
        self.console.print(f"You chose: [bold yellow]{choice}[/bold yellow]")

    def get_navigation_between_questions(self) -> None:
        self.console.print(
            "[P] Prev   [N] Next   [M] Mark for Review   [S] Submit",
            style="bold yellow",
        )

    # ----- User Profile -----
    def show_profile(self, user):
        self.print_title("User Profile", color="magenta")
        if user:
            self.console.print(f"[bold]Username:[/bold] {user.username}")
            self.console.print(f"[bold]Role:[/bold] {user.role}")
        else:
            self.show_error("No user is currently logged in.")
        self.print_divider()
