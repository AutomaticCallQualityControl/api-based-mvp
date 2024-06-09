import json
import tempfile

import streamlit as st
from pydub import AudioSegment


def play_audio_segment(audio_file_bytes, file_type, start_time, end_time):
    with tempfile.NamedTemporaryFile(
        delete=False, suffix=f".{file_type.split('/')[-1]}"
    ) as temp_audio_file:
        temp_audio_file.write(audio_file_bytes)
        temp_audio_file.flush()
        audio = AudioSegment.from_file(temp_audio_file.name)
        segment = audio[start_time * 1000 : end_time * 1000]
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_file:
            segment.export(temp_file.name, format="wav")
            st.audio(temp_file.name, format="audio/wav")


st.title("Результаты Анализа")

if "audio_file" in st.session_state and "output_path" in st.session_state:
    audio_file_bytes = st.session_state.audio_file
    audio_file_type = st.session_state.audio_file_type

    output_path = st.session_state.output_path
    result_json_path = "/Users/a.slavutin/PetProjects/api-based-mvp/data/test_output_4.json"  # f"{output_path}.json"
    transcription_path = "/Users/a.slavutin/PetProjects/api-based-mvp/data/test_dump.json"  # st.session_state.transcription_result_path

    with open(transcription_path, "r", encoding="utf-8") as f:
        transcription = json.load(f)

    with open(result_json_path, "r", encoding="utf-8") as f:
        results = json.load(f)

    # TODO: Handle nested results properly
    # Check out if it nested because of postprocessing either model output
    for idx, result in enumerate(results[0]):
        question = result["question"]
        answer = result["answer"]
        segment_ids = result["segment_id"]
        st.subheader(f"Вопрос: {question}")
        st.write(f"Ответ: {answer}")
        for segment_idx, segment_id in enumerate(segment_ids):
            segment = transcription[int(segment_id)]
            if st.button(
                f"Отрывок релевантный вопросу (ID: {segment_id})", key=f"{idx}-{segment_idx}"
            ):
                play_audio_segment(
                    audio_file_bytes, audio_file_type, segment["start"], segment["end"]
                )
else:
    st.error("Пока пусто, попробуйте загрузить файлы и запустить распознование")
