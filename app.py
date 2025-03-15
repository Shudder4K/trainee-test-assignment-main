from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel
import os
import json
import openai
import uuid
from worker import parse_data
from dotenv import load_dotenv

# Завантаження змінних середовища
load_dotenv()

app = FastAPI()

# Отримання API-ключа OpenAI з .env
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    raise ValueError("OPENAI_API_KEY is not set!")

# Оновлений виклик OpenAI для версії >=1.0.0
openai_client = openai.OpenAI(api_key=openai_api_key)

# Збереження статусу завдань
task_statuses = {}

# Базова директорія проєкту
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def get_file_path(directory: str, filename: str) -> str:
    """ Формування шляху до файлу """
    return os.path.join(BASE_DIR, "data", directory, f"{filename}.txt")


class ProcessInputs(BaseModel):
    topic: str
    document_id: str


class ChatInputs(BaseModel):
    session_id: str
    document_id: str
    text: str


def load_document(document_id: str) -> str:
    """ Завантаження тексту документа """
    file_path = get_file_path("documents", document_id)
    if not os.path.exists(file_path):
        return "Document not found."
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()


def load_chat_history(session_id: str) -> list:
    """ Завантаження історії чату """
    session_file = get_file_path("sessions", session_id).replace(".txt", ".json")
    if os.path.exists(session_file):
        with open(session_file, "r", encoding="utf-8") as file:
            return json.load(file)
    return []


def save_chat_history(session_id: str, message: dict):
    """ Збереження історії чату """
    session_file = get_file_path("sessions", session_id).replace(".txt", ".json")
    os.makedirs(os.path.dirname(session_file), exist_ok=True)
    history = load_chat_history(session_id)
    history.append(message)
    with open(session_file, "w", encoding="utf-8") as file:
        json.dump(history, file, indent=4)


def get_chatgpt_response(document_text: str, chat_history: list, user_input: str) -> str:
    """ Отримання відповіді від OpenAI """
    messages = [{"role": "system", "content": "Use the following document as your knowledge base: " + document_text}]
    messages += chat_history
    messages.append({"role": "user", "content": user_input})

    try:
        response = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        return response.choices[0].message.content
    except openai.OpenAIError as e:
        return f"ChatGPT Error: {str(e)}"


def background_task(task_id: str, topic: str, document_id: str):
    """ Обробка даних у фоновому режимі """
    try:
        task_statuses[task_id] = "running"
        parse_data(topic, document_id)
        task_statuses[task_id] = "finished"
    except Exception:
        task_statuses[task_id] = "failed"


@app.post("/api/v1/process")
def process(inputs: ProcessInputs, background_tasks: BackgroundTasks):
    """ Запуск фонового завдання для обробки Wikipedia """
    task_id = str(uuid.uuid4())
    task_statuses[task_id] = "pending"
    background_tasks.add_task(background_task, task_id, inputs.topic, inputs.document_id)
    return {"task_id": task_id}


@app.get("/api/v1/status/{task_id}")
def get_status(task_id: str):
    """ Отримання статусу фонового завдання """
    status = task_statuses.get(task_id, "not found")
    return {"status": status}


@app.post("/api/v1/chat")
def chat(inputs: ChatInputs):
    """ Чат із GPT на основі документа та історії """
    document_text = load_document(inputs.document_id)
    if document_text == "Document not found.":
        return {"message": "Document not found."}

    chat_history = load_chat_history(inputs.session_id)
    response = get_chatgpt_response(document_text, chat_history, inputs.text)

    save_chat_history(inputs.session_id, {"role": "user", "content": inputs.text})
    save_chat_history(inputs.session_id, {"role": "assistant", "content": response})

    return {"response": response}