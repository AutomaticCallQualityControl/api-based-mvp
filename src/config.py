from typing import Optional

from pydantic_settings import BaseSettings


class Config(BaseSettings):
    # FastWhisper settings
    fastwhisper_device: str = "cpu"
    fastwhisper_model_size: str = "large-v2"
    fastwhisper_beam_size: int = 1
    fastwhisper_lang: str = "ru"
    fastwhisper_compute_type: str = "int16"
    fastwhisper_dump_res_asr_folder: Optional[str] = "/path/to/dump/folder/"

    # TextAnalyzer settings
    textanalyzer_model_type: str = "gpt-3.5-turbo"
    textanalyzer_openai_key: str

    # Application settings
    app_debug: bool = True

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


CONFIG = Config()
