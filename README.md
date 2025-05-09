# PyExam CLI

## Overview

**PyExam CLI** is a command-line application designed for managing and taking exams. It provides a user-friendly interface for students to register, log in, take exams, and view their results — all from your terminal. The application is built in Python with a modular design, making it easy to maintain and scale.

## Features

-   🧑‍🎓 User registration and login
-   📝 Exam management system
-   📊 Result viewing
-   🎨 Styled terminal output using `rich`
-   🗃️ SQLite-based storage (no external DB required)
-   🔧 Modular architecture for clean separation of concerns
-   💻 Command-line interface with helpful prompts
-   🚀 Smooth and simple user experience

## Requirements

-   Python 3.13 or higher
-   [`rich`](https://pypi.org/project/rich/) library (for beautiful CLI output)
-   SQLite3 (bundled with Python)

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/RupeshBhandari/pyexam-cli.git
    ```

2. Navigate to the project directory:

    ```bash
    cd pyexam-cli
    ```

3. Install required libraries:

    ```bash
    pip install rich
    ```

4. Run the application:

    ```bash
    python main.py
    ```

## Usage

1. Launch the app with:

    ```bash
    python main.py
    ```

2. Register or log in via the prompts.

3. After logging in, you can:

    - Take exams
    - View results
    - Navigate easily using CLI options

4. Use the `help` command to see available commands and actions.

## Design Architecture

```mermaid
classDiagram
    %% Core Model Classes
    class User {
        +username: str
        -_password_hash: str
        -_role: str
        +role() [property]
        +to_dict()
        +from_dict(data)
    }

    class Exam {
        +exam_id: int
        +name: str
        +date: str
        +duration: int
        +questions_count: int
        +created_by: User
        +to_dict()
        +from_dict(data)
    }

    %% Manager Classes
    class UserManager {
        -database: DatabaseManager
        +create_user(username, password, role)
        +get_user(username)
        +register(username, password, role)
    }

    class ExamManager {
        -ui: UI
        -input_handler: InputHandler
        -auth: AuthManager
        -exam: Exam
        +add_exam()
        +remove_exam(exam_name)
        +list_exams()
    }

    class AuthManager {
        -_user_manager: UserManager
        -_current_user: User
        -_is_authenticated: bool
        -logger: Logger
        +login(username, password)
        +get_current_user()
    }

    class DatabaseManager {
        -database_name: str
        -database_path: str
        -db: SQLiteDatabase
        +execute(query, params)
        +fetchall()
        +fetchone()
        +retrieve_database_settings(key, file_path)
    }

    %% Interface Classes
    class Navigation {
        -logger: Logger
        -ui: UI
        -input_handler: InputHandler
        -user_manager: UserManager
        -database_manager: DatabaseManager
        -auth_manager: AuthManager
        -exam_manager: ExamManager
        +start()
        +post_login_menu()
        +login()
        +register()
        +start_exam()
        +show_profile()
        +exit()
    }

    class UI {
        -console: Console
        +print_title(title, color)
        +print_divider()
        +ask_input(message)
        +show_success(message)
        +show_error(message)
        +show_info(message)
        +show_main_menu()
        +show_post_login_menu(is_admin)
        +show_login_menu()
        +show_profile(user)
    }

    class InputHandler {
        -input_source: Callable
        -ui: UI
        +get_menu_choice()
        +get_username()
        +get_password()
        +get_email()
        +get_exam_title()
        +get_exam_duration()
    }

    %% Authentication Classes
    class Auth {
        -user: User
        -_password_hash: str
        +check_password(stored_hash)
        +_hash_password(password)
    }

    %% Database Classes
    class Database {
        <<abstract>>
        +connect()
        +execute(query, params)
        +fetchall()
        +fetchone()
        +commit()
        +close()
    }

    class SQLiteDatabase {
        -db_name: str
        -db_path: str
        -conn
        -cursor
        +connect()
        +execute(query, params)
        +fetchall()
        +fetchone()
        +commit()
        +close()
    }

    %% Utility Classes
    class Logger {
        -logger
        +debug(message, user)
        +info(message, user)
        +warning(message, user)
        +error(message, user)
        +critical(message, user)
    }

    %% Relationships
    Database <|-- SQLiteDatabase : implements
    DatabaseManager o-- SQLiteDatabase : uses
    
    Navigation --> UI : uses
    Navigation --> InputHandler : uses
    Navigation --> AuthManager : uses
    Navigation --> UserManager : uses 
    Navigation --> ExamManager : uses
    Navigation --> DatabaseManager : uses
    Navigation --> Logger : uses
    
    AuthManager --> UserManager : uses
    AuthManager o-- User : stores current
    AuthManager --> Logger : uses
    
    Auth --> User : authenticates
    
    UserManager --> DatabaseManager : uses
    UserManager --> User : creates
    
    ExamManager --> Exam : manages
    Exam --> User : references
    
    InputHandler --> UI : uses
    
    UI ..> User : displays data
    UI ..> Exam : displays data
    
    SQLiteDatabase --> DatabaseManager : provides connection
    
    Logger o-- Logger : singleton
```

---

```mermaid
flowchart TD
   MAIN_MENU_OPTIONS --> STUDENT_MENU_OPTIONS
   MAIN_MENU_OPTIONS --> ADMIN_MENU_OPTIONS
   STUDENT_MENU_OPTIONS -->|1| START_EXAM_OPTIONS
   STUDENT_MENU_OPTIONS -->|2| PROFILE_MENU_OPTIONS
   STUDENT_MENU_OPTIONS -->|3| LOGOUT_OPTIONS
   STUDENT_MENU_OPTIONS -->|4| EXIT_OPTIONS
   ADMIN_MENU_OPTIONS -->|1| ADD_EXAM_OPTIONS
   ADMIN_MENU_OPTIONS -->|2| REGISTER_USER_OPTIONS
   ADMIN_MENU_OPTIONS -->|3| DEREGISTER_USER_OPTIONS
   ADMIN_MENU_OPTIONS -->|4| VIEW_ALL_USERS_OPTIONS
   ADMIN_MENU_OPTIONS -->|5| LOGOUT_OPTIONS
   ADMIN_MENU_OPTIONS -->|6| EXIT_OPTIONS
   ADMIN_MENU_OPTIONS -->|7| EXIT_APPLICATION_OPTIONS
```

### Database Schema

## Contributing

We welcome contributions to **PyExam CLI**!

1. Fork the repository.
2. Create a new branch for your feature or fix.
3. Commit your changes with clear messages.
4. Push to your forked repository.
5. Open a pull request to the `main` branch.
6. Ensure your code follows project standards and passes tests (if any).

## License

This project is licensed under the MIT License.  
You are free to use, modify, and distribute this software with proper attribution.

---
