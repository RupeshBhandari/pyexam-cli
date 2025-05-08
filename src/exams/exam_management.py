from .exam import Exam
from src.storage import json_storage

class ExamManagement:
    def __init__(self):
        self.exams = []

    def add_exam(self, exam_details):
        """Add a new exam to the list."""
        self.exams.append(Exam.from_dict(exam_details))
        print(f"Exam '{exam_details['name']}' added successfully.")

    def remove_exam(self, exam_name):
        """Remove an exam from the list."""
        for exam in self.exams:
            if exam['name'] == exam_name:
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