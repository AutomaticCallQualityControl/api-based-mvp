import tempfile

import streamlit as st
from pydub import AudioSegment


def save_uploaded_file(uploaded_file):
    """Save uploaded file to a temporary file and return the path."""
    with tempfile.NamedTemporaryFile(
        delete=False, suffix=f".{uploaded_file.name.split('.')[-1]}"
    ) as temp_file:
        temp_file.write(uploaded_file.getbuffer())
        return temp_file.name


def play_audio_segment(audio_file_path, start_time, end_time, offset=1000):
    """Play an audio segment from the given file between start_time and end_time."""
    audio = AudioSegment.from_file(audio_file_path)
    segment = audio[start_time * 1000 - offset : end_time * 1000 + offset]
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_file:
        segment.export(temp_file.name, format="wav")
        st.audio(temp_file.name, format="audio/wav")
