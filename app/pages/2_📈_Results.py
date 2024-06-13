import json
import os
import tempfile

import pandas as pd
import streamlit as st

from app.audio_utils import play_audio_segment

st.title("Результаты Анализа")

if "audio_file" in st.session_state:
    audio_file_bytes = st.session_state.audio_file
    audio_file_type = st.session_state.audio_file_type
    results = st.session_state.answers
    transcription = st.session_state.transcription
    result_csv_path = st.session_state.result_csv_path

    with tempfile.NamedTemporaryFile(
        delete=False, suffix=f".{audio_file_type.split('/')[-1]}"
    ) as temp_audio_file:
        temp_audio_file.write(audio_file_bytes)
        temp_audio_file_path = temp_audio_file.name

    for result in results[0]:
        if "call_summary" in result:
            st.markdown(
                f"<p style='font-size: 22px; line-height: 2;'>Общее Резюме Звонка:<br/>{result['call_summary']}</p>",
                unsafe_allow_html=True,
            )
            st.write("")  # Add space after call summary

    if result_csv_path:
        st.header("Результаты в формате CSV:")
        try:
            df = pd.read_csv(result_csv_path)
            st.write(df)

            # Download button for CSV
            csv_download_filename = os.path.basename(result_csv_path)
            st.download_button(
                label="Скачать CSV файл",
                data=df.to_csv(index=False).encode("utf-8"),
                file_name=csv_download_filename,
                mime="text/csv",
            )
        except Exception as e:
            st.error(f"Ошибка при чтении CSV файла: {e}")

    st.write("")  # Add space after call summary

    st.header("Подробный разбор каждого вопроса с релевантным отрывком:")

    # TODO: Handle nested results properly
    # Check out if it nested because of postprocessing either model output
    for idx, result in enumerate(results[0]):
        if "call_summary" in result:
            continue

        question = result["question"]
        answer = result["answer"]
        segment_ids = result["segment_id"]
        st.subheader(f"Вопрос: {question}")
        st.write(f"Ответ: {answer}")
        for segment_idx, segment_id in enumerate(segment_ids):
            if isinstance(segment_id, str) and segment_id.startswith("ID "):
                segment_id = segment_id.replace("ID ", "")
            segment = transcription[int(segment_id)]
            if st.button(
                f"Отрывок релевантный вопросу (ID: {segment_id})", key=f"{idx}-{segment_idx}"
            ):
                play_audio_segment(temp_audio_file_path, segment["start"], segment["end"])
        # Clean up the temporary file
    os.remove(temp_audio_file_path)
else:
    st.error("Пока пусто, попробуйте загрузить файлы и запустить распознование")
