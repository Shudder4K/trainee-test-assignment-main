import wikipediaapi
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def get_file_path(directory: str, filename: str) -> str:
    """ Формує коректний шлях до файлу. """
    return os.path.join(BASE_DIR, "data", directory, f"{filename}.txt")

def retrieve_wikipedia_content(topic: str) -> str:
    """ Отримує текст зі сторінки Wikipedia """
    wiki_wiki = wikipediaapi.Wikipedia(
        user_agent="MyFastAPIApp/1.0 (contact: myemail@example.com)",
        language="en"
    )
    page = wiki_wiki.page(topic)

    if not page.exists():
        return f"No Wikipedia page found for topic: {topic}"

    return page.text

def parse_data(topic: str, document_id: str):
    """
    Отримує вміст Wikipedia та зберігає його у файл.
    :param topic: тема пошуку.
    :param document_id: ім'я файлу для збереження.
    """
    content = retrieve_wikipedia_content(topic)

    file_path = get_file_path("documents", document_id)
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    with open(file_path, "w", encoding="utf-8") as file:
        file.write(content)

    print(f" Document saved: {file_path}")


