from abc import ABC, abstractmethod
class AIClient(ABC):
    @abstractmethod
    def get_a_hint (self, question, code=""):
        pass
    @abstractmethod
    def get_a_question (self, question, code=""):
        pass
    @abstractmethod
    def get_a_solution (self, question, code=""):
        pass
