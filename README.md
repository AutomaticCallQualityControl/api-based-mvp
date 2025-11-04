# Call Center Quality Control Automation

An automated solution for evaluating the quality of call center operators' performance. This system transcribes call recordings and analyzes them using AI to assess operator effectiveness, compliance, and customer service quality.

## Purpose

Automate the quality control process for call center operators by:
- Transcribing call recordings using speech recognition APIs
- Analyzing conversations with AI to evaluate operator performance
- Identifying areas for improvement and compliance issues
- Providing objective, consistent quality assessments

## Data Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                          INPUT                                   │
├─────────────────────────────────────────────────────────────────┤
│  1. Audio Recording (.mp3)                                       │
│  2. Evaluation Criteria Document (questions.csv/.txt)            │
│     Pre-compiled questions for operator quality assessment       │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                   STEP 1: TRANSCRIPTION                          │
├─────────────────────────────────────────────────────────────────┤
│  Speech Recognition API (Whisper)                                │
│  • Converts audio to text                                        │
│  • Identifies speakers                                           │
│  • Output: transcription.json                                    │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                   STEP 2: AI ANALYSIS                            │
├─────────────────────────────────────────────────────────────────┤
│  OpenAI Text Analyzer                                            │
│  • Loads evaluation criteria questions                           │
│  • Analyzes transcription against each criterion                 │
│  • Evaluates operator performance                                │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                        OUTPUT                                    │
├─────────────────────────────────────────────────────────────────┤
│  • results.json - Detailed analysis in JSON format               │
│  • results.csv  - Tabular results for easy review                │
│                                                                   │
│  Contains answers to all evaluation criteria questions           │
└─────────────────────────────────────────────────────────────────┘
```

## Sample Evaluation

### Input: Evaluation Criteria (questions.csv)

```
"Приветствие (Поздоровалась ли). Варианты ответа: ДА/НЕТ"
"Имя администратора. Варианты ответа: Имя"
"Было ли два любых уточняющих вопроса. Варианты ответа: ДА/НЕТ"
"Администратор уточнил, как обращаться к Пациенту. Варианты ответа: ДА/НЕТ"
```

*Translation:*
- Did the operator greet the customer? (YES/NO)
- Operator's name
- Were two clarifying questions asked? (YES/NO)
- Did the operator ask how to address the patient? (YES/NO)

### Output: Evaluation Results (results.json)

```json
[
    [
        {
            "question": "Приветствие (Поздоровалась ли).",
            "answer": "ДА",
            "segment_id": "0"
        },
        {
            "question": "Имя администратора",
            "answer": "Юлия",
            "segment_id": "0"
        },
        {
            "question": "Было ли два любых уточняющих вопроса",
            "answer": "ДА",
            "segment_id": "2"
        },
        {
            "question": "Администратор уточнил, как обращаться к Пациенту",
            "answer": "НЕТ",
            "segment_id": "2"
        }
    ]
]
```

**Analysis Summary:**
- ✅ Operator greeted the customer properly
- ✅ Operator identified herself as "Юлия" (Yulia)
- ✅ Two clarifying questions were asked
- ❌ Operator did not ask how to address the patient

## User Interface

The project includes a simple Streamlit-based UI application for easy analysis review. The interface allows you to:
- View detailed breakdown of each evaluation question
- Listen to relevant audio segments for each answer
- Review answers with corresponding transcript excerpts

![UI Example](data/ui.png)

The UI displays each question with its answer and provides audio playback of the relevant conversation segments, making it easy to verify the AI's analysis and conduct quality reviews.

## Setup

1. install reqs

```bash
pip install -r requirements.txt
```

2. Initialize ```pre-commit```

```bash
pre-commit install
```
