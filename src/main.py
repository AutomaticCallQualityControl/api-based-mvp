from speech_recognition.insanely_whisper import InsanelyWhisper
import lazycon
import argparse

parser = argparse.ArgumentParser(description="ASR + ChatGPT")

parser.add_argument(
    "--audio_path",
    required=True,
    type=str,
    help="Path to the audio file to be transcribed.",
)
parser.add_argument(
    "--config_path",
    required=True,
    default="../configs/base.config",
    type=str,
    help='Path to config for ASR and ChatGPT.',
)

parser.add_argument(
    "--dump_path",
    required=False,
    default=None,
    type=str,
    help='Path to .json dump ASR results.',
)

def main():
    args = parser.parse_args()
    cfg = lazycon.load(args.config_path)
    asr_infer = InsanelyWhisper(cfg)
    asr_infer.transcribe_dump(args.audio_path, args.dump_path)

if __name__ == "__main__":
    main()