class Exam:
    def __init__(self, exam_id: int, name: str, date: str, duration: int):
        self.exam_id = exam_id
        self.name = name
        self.date = date
        self.duration = duration

    def __repr__(self):
        return f"Exam({self.exam_id}, {self.name}, {self.date}, {self.duration})"