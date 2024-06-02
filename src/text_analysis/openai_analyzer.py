import json
import re
from typing import List

import pandas as pd
from loguru import logger
from openai import OpenAI

from text_analysis.base import BaseTextAnalyzer
from text_analysis.consts import SYSTEM_MESSAGE_FOR_AUDIO_ANALYSIS


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

    def parse_model_output_to_json(self, content):
        corrected_content = content.replace("'", '"')
        corrected_content = re.sub(r"\}\s*\{", "}, {", corrected_content)
        corrected_content = f"[{corrected_content}]"

        try:
            json_output = json.loads(corrected_content)
            return json_output
        except json.JSONDecodeError as e:
            logger.error("Failed to decode JSON:", e)
            return None

    def generate_report(
        self, transcribed_text: str, id_to_text: dict, csv_path: str, json_out: str
    ) -> None:
        questions_df = pd.read_csv(csv_path)
        questions = questions_df.columns.tolist()

        messages = [{"role": "system", "content": SYSTEM_MESSAGE_FOR_AUDIO_ANALYSIS}]
        messages.append({"role": "user", "content": transcribed_text})

        for question in questions:
            question_prompt = f"Question: {question}"
            messages.append({"role": "user", "content": question_prompt})

        print(messages)
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0.0,
            max_tokens=150 * len(questions),
        )
        result_content = response.choices[0].message.content

        print("Raw response:", result_content)

        structured_responses = self.parse_model_output_to_json(result_content)
        with open(json_out, "w", encoding="utf-8") as f:
            json.dump(structured_responses, f, indent=4, ensure_ascii=False)


openai_key = "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"
csv_path = "/Users/a.slavutin/PetProjects/api-based-mvp/data/test.csv"
csv_path_out = "/Users/a.slavutin/PetProjects/api-based-mvp/data/test_output.json"
json_path = "/Users/a.slavutin/PetProjects/api-based-mvp/data/test_dump.json"

analyzer = TextAnalyzer(openai_key)
formatted_transcript, id_to_text = analyzer.load_and_format_transcription(json_path)
analyzer.generate_report(formatted_transcript, id_to_text, csv_path, csv_path_out)
