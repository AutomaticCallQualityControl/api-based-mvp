import json
import re
from typing import List

import pandas as pd
from openai import OpenAI

from text_analysis.base import BaseTextAnalyzer


class TextAnalyzer(BaseTextAnalyzer):
    def __init__(self, openai_key: str):
        self.client = OpenAI(api_key=openai_key)

    def load_and_format_transcription(self, json_path: str) -> (str, dict):
        """Loads transcription data from a JSON file and formats it into a single transcript,
        assigning an ID to each segment.
        """
        with open(json_path, "r", encoding="utf-8") as file:
            transcript_data = json.load(file)

        formatted_transcript = ""
        id_to_text = {}
        for i, segment in enumerate(transcript_data):
            speaker_id = 1 if i % 2 == 0 else 2  # Simplified speaker ID assignment
            speaker_label = f"Speaker {speaker_id}"
            formatted_transcript += f"{speaker_label} (ID {i}): {segment['text'].strip()} "
            id_to_text[i] = segment["text"].strip()

        return formatted_transcript, id_to_text

    def generate_report(
        self, transcribed_text: str, id_to_text: dict, csv_path: str, csv_out: str
    ) -> None:
        """Generates answers for questions based on the provided transcript and saves the answers with the ID of the
        transcript segments back into the CSV file.
        """
        questions_df = pd.read_csv(csv_path)
        questions = questions_df.columns.tolist()

        # Prepare conversation with context introduction
        messages = [
            {
                "role": "system",
                "content": "This is a transcript of a conversation. Answer the following questions based on the transcript provided.",
            },
            {"role": "user", "content": transcribed_text},
        ]

        # Include each question as a separate user message
        for question in questions:
            messages.append(
                {
                    "role": "user",
                    "content": f"Question: {question} (Include the ID of the relevant transcript segment in your answer.)",
                }
            )

        # Call the model and collect all answers in a single interaction
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0.0,
            max_tokens=150 * len(questions),  # Adjust max tokens based on number of questions
        )

        print(response)

        answers = self.parse_answers(response.choices[0].message.content, questions)

        # Save answers and IDs to CSV
        answers_df = pd.DataFrame(
            {
                "Question": questions,
                "Answer": [ans["text"] for ans in answers],
                "Segment IDs": [ans["id"] for ans in answers],
            }
        )
        answers_df.to_csv(csv_out, index=False)

    def parse_answers(self, answer_content, questions):
        # Use regex to match patterned responses
        pattern = r"\d+\.\s.*?(?=\n\d+\.|$)"
        matches = re.findall(pattern, answer_content)
        answers = [{"text": m, "id": "".join(filter(str.isdigit, m))} for m in matches]

        # Ensure the answers align with the number of questions
        while len(answers) < len(questions):
            answers.append({"text": "No answer provided", "id": "N/A"})

        return answers[: len(questions)]  # Ensure no excess answers


openai_key = "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"
csv_path = "/Users/a.slavutin/PetProjects/api-based-mvp/data/test.csv"
csv_path_out = "/Users/a.slavutin/PetProjects/api-based-mvp/data/test_output.csv"
json_path = "/Users/a.slavutin/PetProjects/api-based-mvp/data/test_dump.json"

analyzer = TextAnalyzer(openai_key)
formatted_transcript, id_to_text = analyzer.load_and_format_transcription(json_path)
analyzer.generate_report(formatted_transcript, id_to_text, csv_path, csv_path_out)
