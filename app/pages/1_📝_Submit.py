from time import sleep

import streamlit as st
from loguru import logger

from app.utils import nav_page
from src.config import CONFIG
from src.speech_recognition.insanely_whisper import InsanelyWhisper
from src.text_analysis.openai_analyzer import TextAnalyzer

st.title("Загрузите файлы для анализа")

audio_file = st.file_uploader("Загрузите аудио файл со звонком", type=["mp3", "wav"])
csv_file = st.file_uploader("Загрузите файл с критериями проверки", type=["csv"])

if "RESULTS_COMPLETED" not in st.session_state:
    st.session_state.RESULTS_COMPLETED = False

if st.button("Загрузить"):
    if audio_file and csv_file:
        # st.session_state.audio_file = audio_file
        st.session_state.audio_file = audio_file.read()
        st.session_state.audio_file_type = audio_file.type
        st.session_state.csv_file = csv_file
        st.session_state.transcription_result_path = "data/test_dump.json"
        st.session_state.output_path = "data/test_output_streamlit"
        logger.info("Processing audio ...")
        sleep(1)
        # asr_infer = InsanelyWhisper(ML_CONFIG.fast_whisper_config)
        # asr_infer.transcribe_dump(st.session_state.audio_file, st.session_state.transcription_result_path)

        logger.info("Processing transcription ...")
        sleep(1)

        # analyzer = TextAnalyzer(openai_key=CONFIG.textanalyzer_openai_key,
        #                         model_type=CONFIG.textanalyzer_model_type)
        # formatted_transcript = analyzer.load_and_format_transcription(st.session_state.transcription_result_path)
        # analyzer.generate_report(formatted_transcript, st.session_state.csv_file, st.session_state.output_path)

        logger.info("Answers recieved ...")

        st.success("Все готово! Результаты можно проверять.")
        st.session_state.RESULTS_COMPLETED = True
    else:
        st.error("Пожалуйста сначала загрузите файлы.")

if st.session_state.RESULTS_COMPLETED and st.button("Результаты"):
    nav_page("results")
