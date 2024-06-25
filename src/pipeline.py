import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import List

import pandas as pd
from loguru import logger

from src.consts import ExtensionType
from src.speech_recognition.insanely_whisper import InsanelyWhisper
from src.text_analysis.openai_analyzer import TextAnalyzer


@dataclass
class AnalysisOutput:
    answers_output: dict
    transcription: dict
    result_csv_path: str
    result_json_path: str


class Pipeline:
    def __init__(self, config):
        self.config = config
        self.output_path = config.output_path
        self.asr_infer = InsanelyWhisper(self.config)
        self.text_analyzer = TextAnalyzer(
            openai_key=self.config.openai_key, model_type=self.config.text_model_type
        )

    def transcribe_audio(self, audio_path: str, transcription_output_path: str):

        logger.info("Processing audio ...")
        transcription = self.asr_infer.transcribe(audio_path=audio_path)
        self.asr_infer.dump_transcription(
            transcription=transcription, dump_path=transcription_output_path
        )
        logger.info("Audio processing completed.")
        return transcription

    # TODO: refactor parameters, merge them
    def analyse_text(
        self, questions: List[str], transcription: dict = None, transcription_path: str = None
    ):
        logger.info("Processing transcription ...")
        if transcription is None and transcription_path is None:
            raise ValueError("Both <transcription> and <transcripton_path> could not be None")

        if transcription is None and transcription_path is not None:
            transcription = self.text_analyzer.load_transcription(json_path=transcription_path)

        formatted_transcript = self.text_analyzer.format_transcription(
            transcript_data=transcription
        )
        answers = self.text_analyzer.get_answers(
            transcribed_text=formatted_transcript, questions=questions
        )
        logger.info("Transcription analysis completed.")
        return answers

    def load_questions(self, questions_path: str) -> List[str]:
        """Loads questions from a CSV or TXT file."""
        file_extension = Path(questions_path).suffix.lower()
        if file_extension == ExtensionType.CSV:
            questions_df = pd.read_csv(questions_path)
            questions = questions_df.columns.tolist()
        elif file_extension == ExtensionType.TXT:
            with open(questions_path, "r", encoding="utf-8") as file:
                questions = [line.strip() for line in file if line.strip()]
        else:
            # flake8: noqa
            raise ValueError(
                f"Unsupported file type {file_extension} for questions. Please provide a CSV or TXT file."
            )

        return questions

    def dump_answers_to_csv(self, output_path, answers: dict):
        transformed_data = {}
        for item in answers[0]:
            # TODO: save summary also
            if "question" not in item.keys():
                continue
            question = item["question"]
            answer = item["answer"]
            if question not in transformed_data:
                transformed_data[question] = []
            transformed_data[question].append(answer)

        max_length = max(len(v) for v in transformed_data.values())
        for key in transformed_data:
            transformed_data[key].extend([None] * (max_length - len(transformed_data[key])))

        df = pd.DataFrame(transformed_data)
        df.to_csv(output_path, index=False)
        logger.info("Store response from OpenAI to csv")

    def dump_answers_to_json(self, output_path, answers: dict):

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(answers, f, indent=4, ensure_ascii=False)

        logger.info("Store response from OpenAI to json")

    def process(self, audio_path, questions_path: str, transcription_output_path: str = None):
        """
        Args:
            audio_path: path to input audio
            questions_path: path to file with OKK questions
        """
        file_name = Path(audio_path).stem
        questions = self.load_questions(questions_path=questions_path)
        if transcription_output_path is None:
            transcription_output_path = os.path.join(
                self.output_path, f"{file_name}_transcription.json"
            )
        result_output_path = os.path.join(self.output_path, f"{file_name}_results")
        csv_out = f"{result_output_path}{ExtensionType.CSV}"
        json_out = f"{result_output_path}{ExtensionType.JSON}"
        if not os.path.exists(transcription_output_path):
            transcription = self.transcribe_audio(
                audio_path, transcription_output_path=transcription_output_path
            )
            answers = self.analyse_text(questions, transcription=transcription)
        else:
            logger.info("Download existing transcription...")
            transcription = self.text_analyzer.load_transcription(
                json_path=transcription_output_path
            )
            answers = self.analyse_text(questions, transcription_path=transcription_output_path)

        if answers and self.config.dump_transcription:
            self.dump_answers_to_csv(output_path=csv_out, answers=answers)
            self.dump_answers_to_json(output_path=json_out, answers=answers)

        return AnalysisOutput(
            answers_output=answers,
            transcription=transcription,
            result_csv_path=csv_out,
            result_json_path=json_out,
        )
