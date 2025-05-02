from abc import ABC, abstractmethod

class Storage(ABC):
    @abstractmethod
    def get_user(self, username: str):
        pass

    @abstractmethod
    def save_user(self, user_data: dict):
        pass

    @abstractmethod
    def get_exam(self, exam_id: str):
        pass

    @abstractmethod
    def store_response(self, user_id: str, exam_id: str, response: dict):
        pass
