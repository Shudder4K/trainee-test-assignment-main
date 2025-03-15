# Використовуємо офіційний образ Python
FROM python:3.9

# Встановлюємо робочу директорію в контейнері
WORKDIR /app

# Копіюємо файли проєкту в контейнер
COPY . /app

# Встановлюємо залежності
RUN pip install --no-cache-dir -r requirements.txt

# Відкриваємо порт 8000 для FastAPI
EXPOSE 8000

# Запускаємо FastAPI через Uvicorn
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
