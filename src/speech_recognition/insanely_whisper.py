from faster_whisper import WhisperModel
from .base import BaseRecognizer
import json, datetime, os
from typing import TypedDict
from tqdm import tqdm

class JsonTranscriptionResult(TypedDict):
    speakers: list
    chunks: list
    text: str


def build_result(outputs) -> JsonTranscriptionResult:
    return {
        "speakers": outputs["speakers"],
        "chunks": outputs["chunks"],
        "text": outputs["text"],
    }

class InsanelyWhisper(BaseRecognizer):
    def __init__(self, config):
        self.beam_size = config.beam_size
        self.lang = config.lang
        self.dump_folder = config.dump_res_asr_folder
        self.model = WhisperModel(config.model_size, device=config.device, compute_type=config.compute_type)

    def dump_results(self, result, dump_path: str):
        with open(dump_path, "w", encoding="utf8") as fp:
            json_result = build_result(result)
            json.dump(json_result, fp, ensure_ascii=False)
        print(f"Your file has been transcribed & speaker segmented go check it out over here: {dump_path}")

    def transcribe(self, audio_path: str):
        pass

    def transcribe_dump(self, audio_path: str, dump_path: str = None) -> str:
        if dump_path is None:
            date = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
            audio_name = os.path.basename(audio_path).split('.')[0]
            file_name = f'{date}_{audio_name}.json'
            dump_path = os.path.join(self.dump_folder, file_name)
        segments, _ = self.model.transcribe(audio_path, beam_size=self.beam_size, language=self.lang)
        print(f'Audio transcribed')
        dump_results = []
        print(f'Diarization:')
        for segment in tqdm(segments):
            dump_results.append({
                'start': segment.start, 'end': segment.end, 'text': segment.text
            })
        with open(dump_path, 'w', encoding="utf8") as f:
            json.dump(dump_results, f, indent=1, ensure_ascii=False)
        print(f'Audio transcribed and diarized, json dump path: {dump_path}')
        # return self.dump_results(segments, dump_path)