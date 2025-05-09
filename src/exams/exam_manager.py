from .exam import Exam
from src.utils.logger import Logger
from src.interface.ui import UI
from src.storage.database_manager import DatabaseManager
from src.user.user_manager import UserManager
from src.interface.input_handler import InputHandler
from src.auth.auth_manager import AuthManager
class ExamManager:
    def __init__(self, 
            ui: UI,
            input_handler: InputHandler, 
            user_manager: UserManager,
            auth_manager: AuthManager,
            database_manager: DatabaseManager,
            logger: Logger ) -> None:
        
        self.ui: UI = ui
        self.input_handler: InputHandler = input_handler
        self.user_manager: UserManager = user_manager
        self.auth_manager: AuthManager = auth_manager
        self.database_manager: DatabaseManager = database_manager
        self.logger: Logger = logger    
        self.exams = []
        
    def add_exam(self):
        self.ui.print_title("Add New Exam", color="green")
        
        # Collect exam data from user
        exam_id = self.input_handler.get_exam_id()
        title = self.input_handler.get_exam_title()
        date = self.input_handler.get_exam_date()
        duration = self.input_handler.get_exam_duration()
        questions_count = self.input_handler.get_exam_questions_count()
        
        # Get current user
        current_user = self.auth_manager.get_current_user()
        created_by = current_user.username if current_user else "admin"
        
        # Create exam directly
        exam = Exam.from_dict({
            "exam_id": exam_id,
            "name": title,
            "date": date,
            "duration": duration,
            "questions_count": questions_count,
            "created_by": created_by,
        })
        
        # Save and add to list
        exam.save_exam()
        self.exams.append(exam)
        self.ui.show_success(f"Exam '{title}' added successfully.")

    def remove_exam(self, exam_name):
        """Remove an exam from the list."""
        for exam in self.exams:
            if exam.name == exam_name:  # Assuming exams are objects with attributes
                self.exams.remove(exam)
                self.ui.show_success(f"Exam '{exam_name}' removed successfully.")
                return
        self.ui.show_error(f"Exam '{exam_name}' not found.")

    def list_exams(self):
        """List all exams."""
        if not self.exams:
            self.ui.show_info("No exams available.")
            return
            
        self.ui.print_title("Available Exams", color="blue")
        for exam in self.exams:
            # Using UI to display consistently formatted exam information
            self.ui.show_info(f"- {exam.name} (Date: {exam.date}, Duration: {exam.duration} min)")