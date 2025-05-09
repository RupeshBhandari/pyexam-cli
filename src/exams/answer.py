from typing import Dict, Any
from datetime import datetime


class Answer:
    """
    Represents a user's answer to an exam question.

    Attributes:
        answer_id (int): Unique identifier for this answer
        question_id (int): ID of the question being answered
        user_answer (int): Index of the option chosen by the user
        is_correct (bool): Whether the answer is correct
        timestamp (datetime): When the answer was submitted
        user_id (str): Username of the user who submitted the answer
    """

    def __init__(
        self,
        answer_id: int,
        question_id: int,
        user_answer: int,
        is_correct: bool,
        exam_id: int,
        user_id: str,
        timestamp: datetime = None,
    ) -> None:
        self.answer_id = answer_id
        self.question_id = question_id
        self.user_answer = user_answer
        self.is_correct = is_correct
        self.exam_id = exam_id
        self.user_id = user_id
        self.timestamp = timestamp or datetime.now()

    def __repr__(self) -> str:
        return f"Answer({self.answer_id}, Q:{self.question_id}, {'✓' if self.is_correct else '✗'})"

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        """Creates an Answer instance from a dictionary."""
        # Parse timestamp if it's a string
        timestamp = data.get("timestamp")
        if isinstance(timestamp, str):
            timestamp = datetime.fromisoformat(timestamp)

        return cls(
            answer_id=data["answer_id"],
            question_id=data["question_id"],
            user_answer=data["user_answer"],
            is_correct=data["is_correct"],
            exam_id=data["exam_id"],
            user_id=data["user_id"],
            timestamp=timestamp,
        )

    def to_dict(self) -> Dict[str, Any]:
        """Converts Answer instance to a dictionary."""
        return {
            "answer_id": self.answer_id,
            "question_id": self.question_id,
            "user_answer": self.user_answer,
            "is_correct": self.is_correct,
            "exam_id": self.exam_id,
            "user_id": self.user_id,
            "timestamp": self.timestamp.isoformat(),
        }
