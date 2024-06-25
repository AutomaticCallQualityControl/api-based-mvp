import json
import re
from typing import List

from loguru import logger
from openai import OpenAI

from src.text_analysis.base import BaseTextAnalyzer
from src.text_analysis.consts import SYSTEM_MESSAGE_FOR_AUDIO_ANALYSIS_RUS


class TextAnalyzer(BaseTextAnalyzer):
    def __init__(self, openai_key: str, model_type: str):
        self.client = OpenAI(api_key=openai_key)
        self.model_type = model_type

    def load_transcription(self, json_path: str) -> dict:
        """Loads transcription data from a JSON file"""
        with open(json_path, "r", encoding="utf-8") as file:
            transcript_data = json.load(file)
        return transcript_data

    def format_transcription(self, transcript_data: dict):
        """Formats transcription into a single transcript, assigning an ID to each segment."""
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

    def get_answers(self, transcribed_text: str, questions: List[str]) -> None:

        messages = [{"role": "system", "content": SYSTEM_MESSAGE_FOR_AUDIO_ANALYSIS_RUS}]
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
        logger.info("Received response from OpenAI")

        structured_responses = self.parse_model_output_to_json(result_content)

        return structured_responses
