import requests


class SonixRecognizer(BaseRecognizer):
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.headers = {"Authorization": f"Bearer {api_key}"}

    def transcribe(self, audio_path: str) -> str:
        """Uploads audio and retrieves transcript in plain text after processing is complete.

        Args:
            audio_path (str): Path to the audio file.

        Returns:
            str: The full text of the transcription.
        """
        media_id = self.upload_audio(audio_path)
        if self.check_media_status(media_id):
            return self.fetch_transcript_text(media_id)
        else:
            return "Transcription failed or is still processing."

    def fetch_transcript_text(self, media_id: str) -> str:
        """Fetches the transcript text for a given media ID.

        Args:
            media_id (str): Media ID of the completed transcription.

        Returns:
            str: The transcript text.
        """
        url = f"https://api.sonix.ai/v1/media/{media_id}/transcript.txt"
        response = requests.get(url, headers=self.headers)
        return response.text

    def upload_audio(self, file_path: str) -> str:
        url = "https://api.sonix.ai/v1/media"
        files = {"file": open(file_path, "rb")}
        data = {"language": "en", "name": "Audio Upload"}
        response = requests.post(url, headers=self.headers, files=files, data=data)
        response_data = response.json()
        return response_data.get("id")

    def check_media_status(self, media_id: str) -> bool:
        url = f"https://api.sonix.ai/v1/media_exports/{media_id}"
        response = requests.get(url, headers=self.headers)
        response_data = response.json()
        return response_data.get("status") == "completed"

    def download_transcript(self, media_id: str) -> str:
        url = f"https://api.sonix.ai/v1/media/{media_id}/transcript.srt"
        response = requests.get(url, headers=self.headers)
        file_path = f"{media_id}.srt"
        with open(file_path, "w") as file:
            file.write(response.text)
        return file_path
