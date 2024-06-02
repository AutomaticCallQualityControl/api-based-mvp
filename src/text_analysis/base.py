from abc import ABC, abstractmethod


class BaseTextAnalyzer(ABC):
    @abstractmethod
    def generate_report(self, transcribed_text: str, questions: str) -> str:
        """Generates a report based on the text and a set of questions.

        Args:
            transcribed_text (str): The text to analyze.
            questions (str): Questions to answer based on the text.

        Returns:
            str: Generated report or answers to the questions.
        """
        pass
