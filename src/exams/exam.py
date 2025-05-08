from src.auth import User
from src.storage import json_storage


class Exam:
    def __init__(
        self,
        exam_id: int,
        name: str,
        date: str,
        duration: int,
        questions_count: int,
        created_by: User,
    ) -> None:
        self.exam_id = exam_id
        self.name = name
        self.date = date
        self.duration = duration
        self.questions_count = questions_count
        self.created_by = created_by
        self.database = json_storage()

    def __repr__(self):
        return f"Exam({self.exam_id}, {self.name}, {self.date}, {self.duration})"

    def get_exam_details(self) -> dict:
        return {
            "exam_id": self.exam_id,
            "name": self.name,
            "date": self.date,
            "duration": self.duration,
            "questions_count": self.questions_count,
            "created_by": self.created_by.username,
        }

    def save_exam(self) -> None:
        exam_data = self.get_exam_details()
        self.database.add_exam(exam_data)

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            exam_id=data["exam_id"],
            name=data["name"],
            date=data["date"],
            duration=data["duration"],
            questions_count=data["questions_count"],
            created_by=data["created_by"],
        )

    def to_dict(self) -> dict:
        return {
            "exam_id": self.exam_id,
            "name": self.name,
            "date": self.date,
            "duration": self.duration,
            "questions_count": self.questions_count,
            "created_by": self.created_by,
        }
