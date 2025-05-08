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
flowchart TD
    A[main.py] --> B[navigator.py]
    B --> C[input_handler.py]
    B --> D[ui.py]

    B --> E[auth.user.py]
    B --> F[exams.exam_manager.py]
    B --> G[logic.evaluator.py]
    B --> H[storage.database.py]

    C -->|Gets user input| B
    D -->|Prints styled output| B
    E -->|Handles login/register| B
    F -->|Handles exam flow| B
    G -->|Scores & results| B
    H -->|Reads/writes data| B
```

### Menu Flow

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

```mermaid
erDiagram
   USER {
         INT id PK
         VARCHAR username
         VARCHAR password
         VARCHAR email
         VARCHAR role
    }
    EXAM {
        INT exam_id PK
        VARCHAR name
        DATE date
        INT duration
        INT questions_count
        INT created_by FK
    }
    USER ||--o{ EXAM : creates
```

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
