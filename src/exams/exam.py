from typing import Dict, Any, Union
from src.user.user import User


class Exam:
    def __init__(
        self,
        exam_id: int,
        name: str,
        date: str,
        duration: int,
        questions_count: int,
        created_by: Union[User, str],
    ) -> None:
        self.exam_id = exam_id
        self.name = name
        self.date = date
        self.duration = duration
        self.questions_count = questions_count
        self.created_by = created_by

    def __repr__(self):
        return f"Exam({self.exam_id}, {self.name}, {self.date}, {self.duration})"

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        return cls(
            exam_id=data["exam_id"],
            name=data["name"],
            date=data["date"],
            duration=data["duration"],
            questions_count=data["questions_count"],
            created_by=data["created_by"],
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "exam_id": self.exam_id,
            "name": self.name,
            "date": self.date,
            "duration": self.duration,
            "questions_count": self.questions_count,
            "created_by": self.created_by,
        }


if __name__ == "__main__":
    # Example usage
    exam = Exam(
        exam_id=1,
        name="Math Exam",
        date="2023-10-01",
        duration=120,
        questions_count=50,
        created_by=User(username="admin", password_hash="admin123"),
    )
    print(exam)
    print(exam.to_dict())
