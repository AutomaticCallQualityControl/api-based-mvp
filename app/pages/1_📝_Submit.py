import os
import tempfile
from time import sleep

import streamlit as st
from loguru import logger

from app.audio_utils import save_uploaded_file
from app.st_utils import nav_page
from src.config import CONFIG
from src.pipeline import Pipeline

st.title("Загрузите файлы для анализа")

audio_file = st.file_uploader("Загрузите аудио файл со звонком", type=["mp3", "wav"])
questions_file = st.file_uploader("Загрузите файл с критериями проверки", type=["csv", "txt"])

if "RESULTS_COMPLETED" not in st.session_state:
    st.session_state.RESULTS_COMPLETED = False

if st.button("Загрузить"):
    if audio_file and questions_file:
        st.session_state.audio_file = audio_file.read()
        st.session_state.audio_file_type = audio_file.type
        st.session_state.questions_file = questions_file

        audio_path = save_uploaded_file(audio_file)
        questions_path = save_uploaded_file(questions_file)
        try:
            logger.info("Initializing pipeline ...")
            pipeline = Pipeline(CONFIG)

            with st.spinner("Обработка... Пожалуйста, подождите..."):
                logger.info("Starting pipeline ...")
                analysis_output = pipeline.process(audio_path, questions_path)

            logger.info("Answers received.")
            st.success("Все готово! Результаты можно проверять.")
            st.session_state.RESULTS_COMPLETED = True
            st.session_state.answers = analysis_output.answers_output
            st.session_state.transcription = analysis_output.transcription
            st.session_state.result_csv_path = analysis_output.result_csv_path

        finally:
            os.remove(audio_path)
            os.remove(questions_path)
    else:
        st.error("Пожалуйста сначала загрузите файлы.")

if st.session_state.RESULTS_COMPLETED and st.button("Результаты"):
    nav_page("results")
