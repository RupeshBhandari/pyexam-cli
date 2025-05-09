from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.text import Text
from rich import box
from rich.align import Align
from rich.table import Table
from rich.layout import Layout
from rich.progress import Progress, SpinnerColumn, TextColumn
from datetime import datetime

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
    "1": "User Management",
    "2": "Exam Management",
    "3": "Logout",
    "4": "Exit",
}

ADMIN_MENU_OPTIONS_USER_MANAGEMENT = {
    "1": "Register New User",
    "2": "Deregister User",
    "3": "View All Users",
    "4": "Update User",
    "5": "View User Profile",
    "6": "Back to Main Menu",
    "7": "Exit",
}

ADMIN_MENU_OPTIONS_EXAM_MANAGEMENT = {
    "1": "Add Exam",
    "2": "View All Exams",
    "3": "Update Exam",
    "4": "Delete Exam",
    "5": "View Exam Results",
    "6": "Back to Main Menu",
    "7": "Exit",
}


class UI:
    _isinstance = None

    def __new__(cls, *args, **kwargs):
        if not cls._isinstance:
            cls._isinstance = super(UI, cls).__new__(cls)
        return cls._isinstance

    def __init__(self) -> None:
        self.console = Console()
        self.show_welcome_banner()

    def show_welcome_banner(self) -> None:
        """Display a welcome banner when the application starts"""
        self.console.clear()
        self.console.print()
        banner = """
        ╔══════════════════════════════════════════════════════════╗
        ║                                                          ║
        ║   ██████╗ ██╗   ██╗███████╗██╗  ██╗ █████╗ ███╗   ███╗   ║
        ║   ██╔══██╗╚██╗ ██╔╝██╔════╝╚██╗██╔╝██╔══██╗████╗ ████║   ║
        ║   ██████╔╝ ╚████╔╝ █████╗   ╚███╔╝ ███████║██╔████╔██║   ║
        ║   ██╔═══╝   ╚██╔╝  ██╔══╝   ██╔██╗ ██╔══██║██║╚██╔╝██║   ║
        ║   ██║        ██║   ███████╗██╔╝ ██╗██║  ██║██║ ╚═╝ ██║   ║
        ║   ╚═╝        ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚═╝   ║
        ║                                                          ║
        ║           Interactive Examination System                 ║
        ║                                                          ║
        ╚══════════════════════════════════════════════════════════╝
        """
        self.console.print(Align.center(banner), style="bold blue")
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.console.print(Align.center(f"Current Time: {current_time}"), style="dim")
        self.console.print()

    # ----- Section Headers -----
    def print_title(self, title: str, color="cyan") -> None:
        panel = Panel(
            Text(title, style="bold"),
            style=f"bold {color}",
            expand=False,
            box=box.ROUNDED,
            border_style=color,
        )
        self.console.print(panel)

    def print_title_center(self, title: str, color="cyan") -> None:
        panel = Panel(
            Align.center(f"[bold]{title}[/bold]"),
            style=f"bold {color}",
            expand=False,
            box=box.ROUNDED,
            border_style=color,
        )
        self.console.print(panel)

    def print_divider(self) -> None:
        self.console.rule(style="dim")

    # ----- Input Prompts -----
    def ask_input(self, message: str) -> str:
        return Prompt.ask(f"[bold magenta]{message}[/bold magenta]")

    def ask_password(self, message: str) -> str:
        return Prompt.ask(f"[bold magenta]{message}[/bold magenta]", password=True)

    # ----- Standardized Messages -----
    def show_success(self, message: str) -> None:
        self.console.print(f"✅ [green]{message}[/green]")

    def show_error(self, message: str) -> None:
        self.console.print(f"❌ [bold red]{message}[/bold red]")

    def show_info(self, message: str) -> None:
        self.console.print(f"ℹ️ [yellow]{message}[/yellow]")

    def show_loading(self, message: str) -> None:
        """Show a loading spinner with message"""
        with Progress(
            SpinnerColumn(),
            TextColumn("[bold blue]{task.description}"),
            transient=True,
        ) as progress:
            progress.add_task(description=message, total=None)
            import time

            time.sleep(1)  # Simulate loading

    # ----- Menu Displays -----
    def create_menu_table(self, menu_options):
        """Create a standardized table for displaying menu options.

        Args:
            menu_options: Dictionary with key-value pairs of menu options

        Returns:
            A Rich Table object formatted for menu display
        """

        table = Table(show_header=False, box=box.ROUNDED, border_style="blue")
        table.add_column("Option", style="cyan")
        table.add_column("Description", style="white")

        for key, value in menu_options.items():
            table.add_row(f"[{key}]", value)

        return table

    def show_main_menu(self) -> None:
        self.console.clear()
        self.print_title("Welcome to PyExam!", color="blue")
        table = Table(show_header=False, box=box.ROUNDED, border_style="blue")
        table.add_column("Option", style="cyan")
        table.add_column("Description", style="white")

        for key, value in MAIN_MENU_OPTIONS.items():
            table.add_row(f"[{key}]", value)

        self.console.print(table)
        self.print_divider()

    def show_post_login_menu(self, is_admin=False) -> None:
        self.console.clear()
        role = "Administrator" if is_admin else "Student"
        self.print_title(f"{role} Menu", color="blue")

        table = Table(show_header=False, box=box.ROUNDED, border_style="blue")
        table.add_column("Option", style="cyan")
        table.add_column("Description", style="white")

        if is_admin:
            for key, value in ADMIN_MENU_OPTIONS.items():
                table.add_row(f"[{key}]", value)
        else:
            for key, value in STUDENT_MENU_OPTIONS.items():
                table.add_row(f"[{key}]", value)

        self.console.print(table)
        self.print_divider()

    def show_exit_message(self) -> None:
        self.console.clear()
        farewell = """
        ┌───────────────────────────────────────┐
        │                                       │
        │       Thank you for using PyExam.     │
        │       Have a great day ahead!         │
        │                                       │
        └───────────────────────────────────────┘
        """
        self.console.print(Align.center(farewell), style="bold green")
        self.print_divider()

    # ----- Login and Registration -----
    def show_login_menu(self) -> None:
        self.console.clear()
        self.print_title("Login to Your Account", color="green")
        self.console.print("[dim]Please enter your credentials below[/dim]")
        self.print_divider()

    def show_login_success(self) -> None:
        self.show_loading("Authenticating...")
        self.show_success("Login successful! Welcome back.")

    def show_login_failure(self) -> None:
        self.show_error("Login failed! Please check your username and password.")
        self.console.print(
            "[dim]Forgot your password? Please contact the administrator.[/dim]"
        )

    def show_register_menu(self) -> None:
        self.console.clear()
        self.print_title("Create New Account", color="green")
        self.console.print("[dim]Please fill in the registration details below[/dim]")
        self.print_divider()

    def show_registration_success(self) -> None:
        self.show_loading("Creating your account...")
        self.show_success("Registration successful! You can now log in.")

    def show_registration_failure(self) -> None:
        self.show_error("Registration failed! Please try again.")

    # ----- Question Presentation -----
    def get_mcq_question(
        self, question_no: int, total_questions: int, question: str, choices: list
    ) -> None:
        self.console.clear()
        progress = f"{question_no}/{total_questions}"
        self.console.rule(
            f"[bold blue]Question {progress} • {int(question_no / total_questions * 100)}% Complete"
        )

        question_panel = Panel(
            Text(question, style="bold white"),
            border_style="blue",
            box=box.ROUNDED,
            title=f"Question {question_no}",
        )
        self.console.print(question_panel)

        options_table = Table(show_header=False, box=box.SIMPLE, padding=(0, 2, 0, 0))
        options_table.add_column("Number", style="cyan bold")
        options_table.add_column("Option", style="white")

        for index, choice in enumerate(choices, start=1):
            options_table.add_row(f"{index}", choice)

        self.console.print(options_table)
        self.print_divider()

    def print_user_choice(self, choice: str) -> None:
        self.console.print(f"You chose: [bold yellow]{choice}[/bold yellow]")

    def get_navigation_between_questions(self) -> None:
        nav_panel = Panel(
            "[P] Previous   [N] Next   [M] Mark for Review   [S] Submit",
            style="bold yellow",
            box=box.SIMPLE,
        )
        self.console.print(nav_panel)

    # ----- User Profile -----
    def show_profile(self, user):
        self.console.clear()
        self.print_title("User Profile", color="magenta")

        if user:
            profile_table = Table(
                show_header=False, box=box.ROUNDED, border_style="magenta"
            )
            profile_table.add_column("Field", style="bold magenta")
            profile_table.add_column("Value", style="white")

            profile_table.add_row("Username", user.username)
            profile_table.add_row("Role", user.role)

            self.console.print(profile_table)

            self.console.print("\n[dim]Press any key to go back to menu...[/dim]")
        else:
            self.show_error("No user is currently logged in.")

        self.print_divider()

    # ----- Exam Results Display -----
    def show_exam_results(
        self, exam_name, correct_count, total_questions, earned_points, total_points
    ):
        self.console.clear()
        self.print_title("Exam Results", color="blue")

        score_percentage = (earned_points / total_points) * 100
        result_status = "PASSED" if score_percentage >= 70 else "FAILED"
        result_color = "green" if score_percentage >= 70 else "red"

        # Create a results table
        results_table = Table(box=box.ROUNDED, border_style="blue")
        results_table.add_column("Category", style="cyan bold")
        results_table.add_column("Result", style="white")

        results_table.add_row("Exam", exam_name)
        results_table.add_row("Correct Answers", f"{correct_count}/{total_questions}")
        results_table.add_row("Points", f"{earned_points}/{total_points}")
        results_table.add_row("Score", f"{score_percentage:.1f}%")
        results_table.add_row(
            "Status", f"[bold {result_color}]{result_status}[/bold {result_color}]"
        )

        self.console.print(results_table)

        # Add some motivational message
        if score_percentage >= 70:
            message = "Congratulations on your success! 🎉"
        else:
            message = "Keep practicing. You'll do better next time! 💪"

        self.console.print(f"\n[bold]{message}[/bold]")
        self.print_divider()
