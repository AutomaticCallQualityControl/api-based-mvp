import json
import re
from typing import List

import pandas as pd
from loguru import logger
from openai import OpenAI

from src.text_analysis.base import BaseTextAnalyzer
from src.text_analysis.consts import SYSTEM_MESSAGE_FOR_AUDIO_ANALYSIS


class TextAnalyzer(BaseTextAnalyzer):
    def __init__(self, openai_key: str, model_type: str):
        self.client = OpenAI(api_key=openai_key)
        self.model_type = model_type

    def load_and_format_transcription(self, json_path: str) -> (str, dict):
        """Loads transcription data from a JSON file and formats it into a single transcript,
        assigning an ID to each segment.
        """
        with open(json_path, "r", encoding="utf-8") as file:
            transcript_data = json.load(file)

        formatted_transcript = ""
        for i, segment in enumerate(transcript_data):
            speaker_id = 1 if i % 2 == 0 else 2  # Simplified speaker ID assignment
            speaker_label = f"Speaker {speaker_id}"
            formatted_transcript += f"{speaker_label} (ID {i}): {segment['text'].strip()} "

        return formatted_transcript

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

    def generate_report(self, transcribed_text: str, csv_path: str, output_path: str) -> None:
        questions_df = pd.read_csv(csv_path)
        questions = questions_df.columns.tolist()

        messages = [{"role": "system", "content": SYSTEM_MESSAGE_FOR_AUDIO_ANALYSIS}]
        messages.append({"role": "user", "content": transcribed_text})

        for question in questions:
            question_prompt = f"Question: {question}"
            messages.append({"role": "user", "content": question_prompt})

        logger.info("Processing input querry to OpenAI...")
        response = self.client.chat.completions.create(
            model=self.model_type,
            messages=messages,
            temperature=0.0,
            max_tokens=150 * len(questions),
        )
        result_content = response.choices[0].message.content
        print(result_content)
        logger.info("Received response from OpenAI")

        structured_responses = self.parse_model_output_to_json(result_content)

        json_out = f"{output_path}.json"
        csv_out = f"{output_path}.csv"
        logger.info("Store response from OpenAI to file")

        with open(json_out, "w", encoding="utf-8") as f:
            json.dump(structured_responses, f, indent=4, ensure_ascii=False)

        if structured_responses:
            df = pd.DataFrame(structured_responses)
            df.to_csv(csv_out, index=False)
        else:
            logger.error("Failed to convert responses to CSV: Invalid JSON data")


# openai_key = "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"
# csv_path = "/Users/a.slavutin/PetProjects/api-based-mvp/data/test.csv"
# csv_path_out = "/Users/a.slavutin/PetProjects/api-based-mvp/data/test_output"
# json_path = "/Users/a.slavutin/PetProjects/api-based-mvp/data/test_dump.json"

# analyzer = TextAnalyzer(openai_key)
# formatted_transcript, id_to_text = analyzer.load_and_format_transcription(json_path)
# analyzer.generate_report(formatted_transcript, id_to_text, csv_path, csv_path_out)
