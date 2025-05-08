from .exam import Exam


class ExamManager:
    def __init__(self):
        self.exams = []

    def add_exam(self):
        self.ui.print_title("Add New Exam", color="green")
        exam_id = self.input_handler.get_exam_id()
        title = self.input_handler.get_exam_title()
        duration = self.input_handler.get_exam_duration()
        questions_count = self.input_handler.get_exam_questions_count()
        created_by = (
            self.auth.get_current_user().username
            if self.auth.get_current_user()
            else "admin"
        )
        exam_data: Exam = self.exam.from_dict(
            {
                "exam_id": exam_id,
                "name": title,
                "date": self.input_handler.get_exam_date(),
                "duration": duration,
                "questions_count": questions_count,
                "created_by": created_by,
            }
        )
        exam_data.save_exam()

    def remove_exam(self, exam_name):
        """Remove an exam from the list."""
        for exam in self.exams:
            if exam["name"] == exam_name:
                self.exams.remove(exam)
                print(f"Exam '{exam_name}' removed successfully.")
                return
        print(f"Exam '{exam_name}' not found.")

    def list_exams(self):
        """List all exams."""
        if not self.exams:
            print("No exams available.")
            return
        print("Available Exams:")
        for exam in self.exams:
            print(f"- {exam['name']} (Date: {exam['date']})")
