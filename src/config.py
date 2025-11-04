from typing import Optional

from pydantic_settings import BaseSettings


class Config(BaseSettings):
    # FastWhisper settings
    whisper_model_size: str = "large-v2"
    whisper_beam_size: int = 1
    whisper_lang: str = "ru"
    whisper_compute_type: str = "int16"
    whisper_dump_res_asr_folder: Optional[str] = "/path/to/dump/folder/"
    dump_transcription: bool = True

    # TextAnalyzer settings
    text_model_type: str = "gpt-3.5-turbo"
    openai_key: str
    dump_text_analyse_results: bool = True

    # Application settings
    app_debug: bool = True
    output_path: str = "data/"
    device: str = "cpu"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


CONFIG = Config()
