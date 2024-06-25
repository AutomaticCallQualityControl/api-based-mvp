import datetime
import json
import os
from typing import TypedDict

from faster_whisper import WhisperModel
from loguru import logger
from tqdm import tqdm

from src.speech_recognition.base import BaseRecognizer

# TODO: We still need it ?
# class JsonTranscriptionResult(TypedDict):
#     speakers: list
#     chunks: list
#     text: str


# def build_result(outputs) -> JsonTranscriptionResult:
#     return {
#         "speakers": outputs["speakers"],
#         "chunks": outputs["chunks"],
#         "text": outputs["text"],
#     }


class InsanelyWhisper(BaseRecognizer):
    def __init__(self, config):
        self.beam_size = config.whisper_beam_size
        self.lang = config.whisper_lang
        self.dump_folder = config.whisper_dump_res_asr_folder
        self.model = WhisperModel(
            config.whisper_model_size,
            device=config.device,
            compute_type=config.whisper_compute_type,
        )

    def dump_transcription(self, transcription, dump_path: str):
        with open(dump_path, "w", encoding="utf8") as fp:
            json.dump(transcription, fp, indent=1, ensure_ascii=False)

    def transcribe(self, audio_path: str):
        segments, _ = self.model.transcribe(
            audio_path, beam_size=self.beam_size, language=self.lang
        )
        logger.info(f"Audio transcribed")
        dump_results = []
        logger.info(f"Diarization...")
        for segment in tqdm(segments):
            dump_results.append({"start": segment.start, "end": segment.end, "text": segment.text})
        return dump_results

    def transcribe_dump(self, audio_path: str, dump_path: str = None) -> str:
        if dump_path is None:
            date = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
            audio_name = os.path.basename(audio_path).split(".")[0]
            file_name = f"{date}_{audio_name}.json"
            dump_path = os.path.join(self.dump_folder, file_name)

        transcription = self.transcribe(audio_path=audio_path)
        if self.config.dump_transcription:
            self.dump_transcription(transcription=transcription, dump_path=dump_path)
            logger.info(f"Transcription saved to json dump path: {dump_path}")
        logger.info(f"Audio transcribed and diarized.")
