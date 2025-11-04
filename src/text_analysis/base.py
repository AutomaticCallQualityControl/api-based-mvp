from abc import ABC, abstractmethod


class BaseTextAnalyzer(ABC):
    @abstractmethod
    def get_answers(self, transcribed_text: str, questions: str) -> str:
        """Extract the answers  based on the text and a set of questions.

        Args:
            transcribed_text (str): The text to analyze.
            questions (str): Questions to answer based on the text.

        Returns:
            str: Generated report or answers to the questions.
        """
        pass
