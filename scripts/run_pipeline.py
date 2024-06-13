import argparse

from src.config import CONFIG
from src.pipeline import Pipeline
from src.speech_recognition.insanely_whisper import InsanelyWhisper

parser = argparse.ArgumentParser(description="ASR + ChatGPT")

parser.add_argument(
    "--audio_path",
    required=True,
    type=str,
    help="Path to the audio file to be transcribed.",
)

parser.add_argument(
    "--questions_path",
    required=True,
    default=None,
    type=str,
    help="Path to .csv or .txt file with questions.",
)


def main():
    args = parser.parse_args()
    pipeline = Pipeline(config=CONFIG)
    print(pipeline.process(audio_path=args.audio_path, questions_path=args.questions_path))


if __name__ == "__main__":
    main()
