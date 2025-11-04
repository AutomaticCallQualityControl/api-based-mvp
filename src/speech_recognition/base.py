from abc import ABC, abstractmethod


class BaseRecognizer(ABC):
    @abstractmethod
    def transcribe(self, audio_path: str) -> str:
        """Transcribes audio to text.

        Args:
            audio_path (str): Path to the audio file.

        Returns:
            str: Transcribed text.
        """
        pass

    @abstractmethod
    def transcribe_dump(self, audio_path: str, dump_path: str) -> str:
        """Transcribes audio to text.

        Args:
            audio_path (str): Path to the audio file.

        Returns:
            str: Path to file with results.
        """
        pass
