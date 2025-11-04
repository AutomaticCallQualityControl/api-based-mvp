import argparse
from pathlib import Path

from loguru import logger

from src.config import CONFIG
from src.pipeline import Pipeline

parser = argparse.ArgumentParser(description="ASR + ChatGPT")

parser.add_argument(
    "--directory_path",
    type=Path,
    help="Path to the directory containing audio files to be transcribed.",
)

parser.add_argument(
    "--audio_path",
    type=Path,
    help="Path to a single audio file to be transcribed.",
)

parser.add_argument(
    "--questions_path",
    required=True,
    type=Path,
    help="Path to .csv or .txt file with questions.",
)


def main():
    args = parser.parse_args()
    pipeline = Pipeline(config=CONFIG)

    def process_audio(audio_path: Path):
        file_name = audio_path.stem
        transcription_file_name = f"{file_name}_transcription.json"
        transcription_output_path = audio_path.parent / transcription_file_name

        result = pipeline.process(
            audio_path=str(audio_path),
            questions_path=str(args.questions_path),
            transcription_output_path=str(transcription_output_path),
        )
        logger.info(f"Processed {file_name}:")
        logger.info(f"  - Transcription saved to: {result.transcription}")
        logger.info(f"  - Results saved to: {result.result_csv_path}, {result.result_json_path}")

    if args.audio_path:
        process_audio(args.audio_path)

    elif args.directory_path:
        for audio_path in args.directory_path.glob("*.mp3"):
            process_audio(audio_path)
    else:
        logger.warning("Either --audio_path or --directory_path must be provided.")
        exit(1)


if __name__ == "__main__":
    main()
