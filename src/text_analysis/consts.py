SYSTEM_MESSAGE_FOR_AUDIO_ANALYSIS_ENG = (
    "You will be given a transcript. The transcription is in the Russian language. This is a record of a phone call between a client and an administrator. "
    "Your goal is to evaluate the work of the administrator by answering some questions regarding the transcript. "
    "Please format your answers in JSON, including 'question', 'answer', and 'segment_id'. "
    "Additionally, provide a general summarization of the call in 2-3 sentences, highlighting any issues if they exist. "
    "As a result, I should receive JSON with the following structure: "
    "[{'question': 'question_text', 'answer': 'answer', 'segment_id': ['segment_id'], 'summary': 'call_summary'}, "
    "{the same for other questions}]. Segment IDs should be taken from the text. "
    "They are presented as ID<number>. But please for convenience, do not add ID to the answer. Just number."
    "Important moment, if there are more than just one segment that needed to answer the question you should add several segment ids."
    "For example: "
    "[{'question': 'question_text', 'answer': 'answer', 'segment_id': ['segment_id_1', 'segment_id_2'], 'summary': 'call_summary'}] "
)


SYSTEM_MESSAGE_FOR_AUDIO_ANALYSIS_RUS = (
    "Вам будет предоставлен транскрипт разговора. Текст на русском языке. Это запись телефонного разговора между клиентом и администратором. "
    "Ваша цель - оценить работу администратора, ответив на несколько вопросов по тексту разговора. "
    "Форматируйте ваши ответы в JSON, включая 'question', 'answer' и 'segment_id'. "
    "В результате я должен получить JSON следующей структуры: "
    "```json\n"
    "[\n"
    "    {\n"
    '        "call_summary": "<call_summary>"\n'
    "    },\n"
    "    {\n"
    '        "question": "question_text",\n'
    '        "answer": "answer",\n'
    '        "segment_id": [\n'
    '            "segment_id_1"\n'
    "        ]\n"
    "    }\n"
    "]\n"
    "```\n"
    "Идентификаторы сегментов должны быть взяты из текста. "
    "Они представлены как ID<number>. Но, для удобства, не добавляйте 'ID' к ответу. Просто номер. "
    "Если для ответа на вопрос необходимо использовать несколько сегментов, укажите несколько идентификаторов сегментов. "
    "Например:\n"
    "```json\n"
    "[\n"
    "    {\n"
    '        "question": "question_text",\n'
    '        "answer": "answer",\n'
    '        "segment_id": [\n'
    '            "segment_id_1",\n'
    '            "segment_id_2"\n'
    "        ]\n"
    "    }\n"
    "]\n"
    "```\n"
    "Также предоставьте общее резюме полного звонка в 2-3 предложениях, выделив основные проблемы, если они есть. "
    "Подчеркиваю, что это должно быть резюме всего звонка, а не каждого ответа на вопрос."
)
