import json
from typing import List, Dict, Any, Optional
from datetime import datetime

from .exam import Exam
from .question import Question
from .answer import Answer
from src.utils.logger import Logger
from src.interface.ui import UI
from src.storage.database_manager import DatabaseManager
from src.user.user_manager import UserManager
from src.interface.input_handler import InputHandler
from src.auth.auth_manager import AuthManager


class ExamManager:
    def __init__(
        self,
        ui: UI,
        input_handler: InputHandler,
        user_manager: UserManager,
        database_manager: DatabaseManager,
        logger: Logger,
        auth_manager=None,
    ) -> None:
        self.ui: UI = ui
        self.input_handler: InputHandler = input_handler
        self.user_manager: UserManager = user_manager
        self.database_manager: DatabaseManager = database_manager
        self.logger: Logger = logger
        self.auth_manager = auth_manager
        self.exams: List[Exam] = []
        self.load_exams()

    def load_exams(self) -> None:
        """Load all exams from the database."""
        try:
            with self.database_manager as db:
                db.execute("SELECT * FROM exams")
                exam_rows = db.fetchall()

            self.exams = []
            for row in exam_rows:
                exam_dict = {
                    "exam_id": row[0],
                    "name": row[1],
                    "date": row[2],
                    "duration": row[3],
                    "questions_count": row[4],
                    "created_by": row[5],
                }
                self.exams.append(Exam.from_dict(exam_dict))

            self.logger.info(f"Loaded {len(self.exams)} exams from database")
        except Exception as e:
            self.logger.error(f"Error loading exams: {str(e)}")
            self.ui.show_error(f"Failed to load exams: {str(e)}")

    def add_exam(self) -> bool:
        """Add a new exam with questions."""
        self.ui.print_title("Add New Exam", color="green")

        try:
            # Get exam metadata
            title = self.input_handler.get_exam_title()
            date = self.input_handler.get_exam_date()
            duration = self.input_handler.get_exam_duration()
            questions_count = self.input_handler.get_exam_questions_count()

            # Get current user as creator
            current_user = self.auth_manager.get_current_user()
            if not current_user:
                self.ui.show_error("No user is currently logged in.")
                return False

            created_by = current_user.username

            # Create new exam ID
            exam_id = self._generate_new_exam_id()

            # Create and save exam
            with self.database_manager as db:
                db.execute(
                    "INSERT INTO exams (exam_id, name, date, duration, questions_count, created_by) "
                    "VALUES (?, ?, ?, ?, ?, ?)",
                    (exam_id, title, date, duration, questions_count, created_by),
                )

            # Add questions
            self.ui.print_title(f"Add {questions_count} Questions", color="cyan")
            for i in range(1, questions_count + 1):
                self._add_question(exam_id, i)

            # Reload exams to include the new one
            self.load_exams()
            self.ui.show_success(
                f"Exam '{title}' with {questions_count} questions added successfully."
            )
            return True

        except Exception as e:
            self.logger.error(f"Error adding exam: {str(e)}")
            self.ui.show_error(f"Failed to add exam: {str(e)}")
            return False
        self.ui.show_success(f"Exam '{title}' added successfully.")

    def _generate_new_exam_id(self) -> int:
        """Generate a new unique exam ID."""
        if not self.exams:
            return 1
        return max(exam.exam_id for exam in self.exams) + 1

    def _add_question(self, exam_id: int, question_number: int) -> None:
        """Add a question to an exam."""
        self.ui.print_title(f"Question {question_number}", color="yellow")

        # Get question details
        question_text = self.ui.ask_input("Enter question text")

        # Get options
        options = []
        option_count = 4  # Default to 4 options per question
        for i in range(1, option_count + 1):
            option = self.ui.ask_input(f"Enter option {i}")
            options.append(option)

        # Get correct answer
        while True:
            correct_answer = self.ui.ask_input(
                f"Enter correct option number (1-{option_count})"
            )
            try:
                correct_answer = int(correct_answer)
                if 1 <= correct_answer <= option_count:
                    break
                self.ui.show_error(
                    f"Please enter a number between 1 and {option_count}"
                )
            except ValueError:
                self.ui.show_error("Please enter a valid number")

        # Adjust for zero-indexed storage
        correct_answer_index = correct_answer - 1

        # Generate question ID
        question_id = self._generate_new_question_id()

        # Save question to database
        try:
            with self.database_manager as db:
                db.execute(
                    "INSERT INTO questions (question_id, text, options, correct_answer, points, exam_id) "
                    "VALUES (?, ?, ?, ?, ?, ?)",
                    (
                        question_id,
                        question_text,
                        json.dumps(options),
                        correct_answer_index,
                        1,
                        exam_id,
                    ),
                )
            self.ui.show_success(f"Question {question_number} added")
        except Exception as e:
            self.logger.error(f"Error adding question: {str(e)}")
            self.ui.show_error(f"Failed to add question: {str(e)}")

    def _generate_new_question_id(self) -> int:
        """Generate a new unique question ID."""
        try:
            with self.database_manager as db:
                db.execute("SELECT MAX(question_id) FROM questions")
                result = db.fetchone()

            max_id = result[0] if result and result[0] is not None else 0
            return max_id + 1
        except Exception as e:
            self.logger.error(f"Error generating question ID: {str(e)}")
            return int(datetime.now().timestamp())  # Fallback to timestamp

    def remove_exam(self, exam_id: int) -> bool:
        """Remove an exam and all its questions."""
        try:
            # Find the exam in memory
            exam = next((e for e in self.exams if e.exam_id == exam_id), None)
            if not exam:
                self.ui.show_error(f"Exam with ID {exam_id} not found.")
                return False

            # Remove from database
            with self.database_manager as db:
                # First remove associated questions
                db.execute("DELETE FROM questions WHERE exam_id = ?", (exam_id,))
                # Then remove the exam
                db.execute("DELETE FROM exams WHERE exam_id = ?", (exam_id,))

            # Remove from memory
            self.exams = [e for e in self.exams if e.exam_id != exam_id]

            self.ui.show_success(f"Exam '{exam.name}' removed successfully.")
            return True
        except Exception as e:
            self.logger.error(f"Error removing exam: {str(e)}")
            self.ui.show_error(f"Failed to remove exam: {str(e)}")
            return False

    def list_exams(self) -> None:
        """List all available exams."""
        if not self.exams:
            self.ui.show_info("No exams available.")
            return

        self.ui.print_title("Available Exams", color="blue")
        for exam in self.exams:
            self.ui.show_info(
                f"ID: {exam.exam_id} - {exam.name} (Date: {exam.date}, Duration: {exam.duration} min, Questions: {exam.questions_count})"
            )

    def get_exam(self, exam_id: int) -> Optional[Exam]:
        """Get an exam by ID."""
        return next((e for e in self.exams if e.exam_id == exam_id), None)

    def get_exam_questions(self, exam_id: int) -> List[Question]:
        """Get all questions for a specific exam."""
        questions = []
        try:
            with self.database_manager as db:
                db.execute("SELECT * FROM questions WHERE exam_id = ?", (exam_id,))
                question_rows = db.fetchall()

            for row in question_rows:
                options = json.loads(row[2])
                question_dict = {
                    "question_id": row[0],
                    "text": row[1],
                    "options": options,
                    "correct_answer": row[3],
                    "points": row[4],
                    "exam_id": row[5],
                }
                questions.append(Question.from_dict(question_dict))

            return questions
        except Exception as e:
            self.logger.error(f"Error getting exam questions: {str(e)}")
            self.ui.show_error(f"Failed to load exam questions: {str(e)}")
            return []

    def take_exam(self, exam_id: int) -> None:
        """Allow a user to take an exam."""
        # Get the exam
        exam = self.get_exam(exam_id)
        if not exam:
            self.ui.show_error(f"Exam with ID {exam_id} not found.")
            return

        # Get the user
        user = self.auth_manager.get_current_user()
        if not user:
            self.ui.show_error("You must be logged in to take an exam.")
            return

        # Get all questions for this exam
        questions = self.get_exam_questions(exam_id)
        if not questions:
            self.ui.show_error("This exam has no questions.")
            return

        # Start the exam
        self.ui.print_title(f"Starting Exam: {exam.name}", color="green")
        self.ui.show_info(f"Duration: {exam.duration} minutes")
        self.ui.show_info(f"Questions: {len(questions)}")
        self.ui.print_divider()

        # Record answers
        answers = []
        for i, question in enumerate(questions, 1):
            answer = self._present_question(question, i, len(questions))
            answers.append(answer)

        # Calculate and show results
        self._show_exam_results(exam, questions, answers)

        # Save answers to database
        self._save_exam_answers(user.username, exam_id, answers)

    def _present_question(self, question: Question, q_num: int, total: int) -> Answer:
        """Present a question to the user and get their answer."""
        # Display the question
        self.ui.get_mcq_question(q_num, total, question.text, question.options)

        # Get user's answer
        while True:
            answer_text = self.ui.ask_input(f"Your answer (1-{len(question.options)})")
            try:
                answer_num = int(answer_text)
                if 1 <= answer_num <= len(question.options):
                    # Convert to zero-based index
                    user_answer = answer_num - 1
                    break
                self.ui.show_error(
                    f"Please enter a number between 1 and {len(question.options)}"
                )
            except ValueError:
                self.ui.show_error("Please enter a valid number")

        # Check if correct
        is_correct = question.is_correct(user_answer)

        # Create answer object
        answer_id = int(datetime.now().timestamp())  # Simple unique ID
        answer = Answer(
            answer_id=answer_id,
            question_id=question.question_id,
            user_answer=user_answer,
            is_correct=is_correct,
            exam_id=question.exam_id,
            user_id=self.auth_manager.get_current_user().username,
        )

        return answer

    def _show_exam_results(
        self, exam: Exam, questions: List[Question], answers: List[Answer]
    ) -> None:
        """Display exam results to the user."""
        correct_count = sum(1 for answer in answers if answer.is_correct)
        total_points = sum(q.points for q in questions)
        earned_points = sum(
            q.points for q, a in zip(questions, answers) if a.is_correct
        )

        self.ui.print_title("Exam Results", color="blue")
        self.ui.show_info(f"Exam: {exam.name}")
        self.ui.show_info(f"Correct Answers: {correct_count}/{len(questions)}")
        self.ui.show_info(f"Points: {earned_points}/{total_points}")
        self.ui.show_info(f"Score: {(earned_points / total_points) * 100:.1f}%")

        # Detailed results
        self.ui.print_title("Question Details", color="yellow")
        for i, (question, answer) in enumerate(zip(questions, answers), 1):
            result = "✓" if answer.is_correct else "✗"
            user_choice = question.options[answer.user_answer]
            correct_choice = question.options[question.correct_answer]

            self.ui.show_info(f"Q{i}: {result} Your answer: {user_choice}")
            if not answer.is_correct:
                self.ui.show_info(f"   Correct answer: {correct_choice}")

    def _save_exam_answers(
        self, username: str, exam_id: int, answers: List[Answer]
    ) -> None:
        """Save exam answers to the database."""
        try:
            with self.database_manager as db:
                for answer in answers:
                    db.execute(
                        "INSERT INTO answers (answer_id, question_id, user_answer, is_correct, exam_id, user_id, timestamp) "
                        "VALUES (?, ?, ?, ?, ?, ?, ?)",
                        (
                            answer.answer_id,
                            answer.question_id,
                            answer.user_answer,
                            answer.is_correct,
                            answer.exam_id,
                            answer.user_id,
                            answer.timestamp.isoformat(),
                        ),
                    )
            self.logger.info(
                f"Saved {len(answers)} answers for user {username} on exam {exam_id}"
            )
        except Exception as e:
            self.logger.error(f"Error saving exam answers: {str(e)}")
            self.ui.show_error(f"Failed to save your answers: {str(e)}")
