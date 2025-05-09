import os
import sqlite3
import json
import hashlib


def setup_database():
    """Set up the database with necessary tables if they don't exist."""
    # Load database config
    with open("config/database.json", "r") as f:
        db_config = json.load(f)

    db_path = db_config["DATABASE"]["path"]

    # Create the directory if it doesn't exist
    os.makedirs(os.path.dirname(db_path), exist_ok=True)

    # Connect to database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Create users table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARY KEY,
        password TEXT NOT NULL,
        role TEXT NOT NULL
    )
    """)

    # Create exams table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS exams (
        exam_id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        date TEXT NOT NULL,
        duration INTEGER NOT NULL,
        questions_count INTEGER NOT NULL,
        created_by TEXT NOT NULL,
        FOREIGN KEY (created_by) REFERENCES users (username)
    )
    """)

    # Create questions table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS questions (
        question_id INTEGER PRIMARY KEY,
        text TEXT NOT NULL,
        options TEXT NOT NULL,
        correct_answer INTEGER NOT NULL,
        points INTEGER NOT NULL DEFAULT 1,
        exam_id INTEGER NOT NULL,
        FOREIGN KEY (exam_id) REFERENCES exams (exam_id)
    )
    """)

    # Create answers table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS answers (
        answer_id INTEGER PRIMARY KEY,
        question_id INTEGER NOT NULL,
        user_answer INTEGER NOT NULL,
        is_correct BOOLEAN NOT NULL,
        exam_id INTEGER NOT NULL,
        user_id TEXT NOT NULL,
        timestamp TEXT NOT NULL,
        FOREIGN KEY (question_id) REFERENCES questions (question_id),
        FOREIGN KEY (exam_id) REFERENCES exams (exam_id),
        FOREIGN KEY (user_id) REFERENCES users (username)
    )
    """)

    # Add default admin user if it doesn't exist
    cursor.execute("SELECT COUNT(*) FROM users WHERE username = 'admin'")
    if cursor.fetchone()[0] == 0:
        admin_password = hashlib.sha256("admin".encode()).hexdigest()
        cursor.execute(
            "INSERT INTO users (username, password, email, role) VALUES (?, ?, ?, ?)",
            ("admin", admin_password, "admin@example.com", "admin"),
        )

    # Commit changes and close connection
    conn.commit()
    conn.close()

    print("Database setup complete.")


if __name__ == "__main__":
    setup_database()
