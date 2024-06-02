from typing import List

import openai
import pandas as pd

from text_analysis.base import BaseTextAnalyzer


class TextAnalyzer(BaseTextAnalyzer):
    def __init__(self, openai_key: str):
        openai.api_key = openai_key

    def generate_report(self, transcribed_text: str, csv_path: str) -> None:
        """
        Uses OpenAI to generate answers for questions loaded from a CSV file's headers,
        based on provided transcribed text, and saves the answers back into the CSV file.

        Args:
            transcribed_text (str): The text to analyze.
            csv_path (str): Path to the CSV file where questions are headers and answers will be filled.
        """
        # Read questions from CSV file headers
        questions_df = pd.read_csv(csv_path)
        questions = questions_df.columns.tolist()

        # Generate answers using OpenAI
        answers = []
        for question in questions:
            prompt = f"{transcribed_text}\n\nQuestion: {question}\nAnswer:"
            response = openai.Completion.create(
                model="text-davinci-003",  # Use the most appropriate and latest model available
                prompt=prompt,
                temperature=0.5,
                max_tokens=150,
            )
            answers.append(response.choices[0].text.strip())

        # Fill CSV with the answers and save it
        answers_df = pd.DataFrame([answers], columns=questions)
        answers_df.to_csv(csv_path, index=False)


openai_key = "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"
transcription = "Today's meeting discussed various strategic initiatives..."
csv_path = "/path/to/your/questions.csv"

analyzer = TextAnalyzer(openai_key)
analyzer.generate_report(transcription, csv_path)
