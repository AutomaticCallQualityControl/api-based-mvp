SYSTEM_MESSAGE_FOR_AUDIO_ANALYSIS = (
    "You will be given a transcript. The transcription is in the Russian language. This is a record of a phone call between a client and an administrator. "
    "Your goal is to evaluate the work of the administrator by answering some questions regarding the transcript. "
    "Please format your answers in JSON, including 'question', 'answer', and 'segment_id'. "
    "As a result, I should receive JSON with the following structure: "
    "[{'question': 'question_text', 'answer': 'answer', 'segment_id': ['segment_id']}, "
    "{the same for other questions}]. Segment IDs should be taken from the text. "
    "They are presented as ID<number>. But please for convenience, do not add ID to the answer. Just number."
    "Important moment, if there are more than just one segment that needed to answer the question you should add several segment ids."
    "For example: "
    "[{'question': 'question_text', 'answer': 'answer', 'segment_id': ['segment_id_1', 'segment_id_2']]}, "
)
