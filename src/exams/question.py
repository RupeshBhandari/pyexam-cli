from typing import List, Dict, Any


class Question:
    """
    Represents an exam question with various properties and answer options.

    Attributes:
        question_id (int): Unique identifier for the question
        text (str): The question text
        options (List[str]): Multiple choice options
        correct_answer (int): Index of the correct answer in options list
        points (int): Point value for this question
        exam_id (int): ID of the exam this question belongs to
    """

    def __init__(
        self,
        question_id: int,
        text: str,
        options: List[str],
        correct_answer: int,
        points: int = 1,
        exam_id: int = None,
    ) -> None:
        self.question_id = question_id
        self.text = text
        self.options = options
        self.correct_answer = correct_answer
        self.points = points
        self.exam_id = exam_id

    def __repr__(self) -> str:
        return f"Question({self.question_id}, '{self.text[:20]}...', {len(self.options)} options)"

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        """Creates a Question instance from a dictionary."""
        return cls(
            question_id=data["question_id"],
            text=data["text"],
            options=data["options"],
            correct_answer=data["correct_answer"],
            points=data.get("points", 1),
            exam_id=data.get("exam_id"),
        )

    def to_dict(self) -> Dict[str, Any]:
        """Converts Question instance to a dictionary."""
        return {
            "question_id": self.question_id,
            "text": self.text,
            "options": self.options,
            "correct_answer": self.correct_answer,
            "points": self.points,
            "exam_id": self.exam_id,
        }

    def is_correct(self, answer_index: int) -> bool:
        """Checks if the provided answer index matches the correct answer."""
        return answer_index == self.correct_answer
