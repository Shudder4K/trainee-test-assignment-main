FastAPI Chat Application

This project is a FastAPI-based application that provides the following functionality:
- Background Task Processor: Fetches information from Wikipedia and stores it in a text file.
- Chat System: Uses OpenAI's GPT to provide responses based on stored documents and chat history.
- Task Status Management: Tracks the status of background tasks.
- Docker & Docker Compose Support: Runs seamlessly in a containerized environment.

Getting Started

Prerequisites
Ensure you have the following installed on your machine:
- Python 3.9+
- Docker & Docker Compose

Installation
1. Clone the repository:
```bash
 git clone https://github.com/your-repo/chat_app.git
 cd chat_app
```

2. Create a virtual environment & install dependencies:
```bash
python -m venv venv
source venv/bin/activate  # For Linux/macOS
venv\Scripts\activate  # For Windows
pip install -r requirements.txt
```

3. Create an `.env` file and set your OpenAI API Key:
```bash
echo "OPENAI_API_KEY=your-openai-key" > .env
```

4. Run the application locally:
```bash
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

Open the API documentation at: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

Running with Docker

1. Build the Docker Image
```bash
docker build -t chat_app .
```

2. Run the Container
```bash
docker run -p 8000:8000 -v $(pwd)/data:/app/data chat_app
```

Running with Docker Compose

1. Start the Application
```bash
docker-compose up -d
```

2. Stop the Application
```bash
docker-compose down
```

API Endpoints

1. Process Wikipedia Topic
POST `/api/v1/process`
```json
{
    "topic": "Python (programming language)",
    "document_id": "python_info"
}
```
Starts a background task to fetch Wikipedia content.

2. Check Task Status
GET `/api/v1/status/{task_id}`
```json
{
    "status": "finished"
}
```
Returns the status of a processing task.

3. Chat with GPT
POST `/api/v1/chat`
```json
{
    "session_id": "session_001",
    "document_id": "python_info",
    "text": "What is Python?"
}
```
Sends a query to GPT based on stored Wikipedia content and chat history.

Project Structure
```
chat_app/
│── app.py                 # Main FastAPI application
│── worker.py              # Wikipedia background processor
│── Dockerfile             # Docker configuration
│── docker-compose.yml     # Docker Compose config
│── requirements.txt       # Python dependencies
│── .env                   # OpenAI API Key (not committed)
│── data/
│   ├── documents/         # Wikipedia articles stored as text files
│   ├── sessions/          # Chat history stored as JSON files
```

Technologies Used
- FastAPI (for API development)
- Uvicorn (for ASGI server)
- OpenAI API (for chatbot functionality)
- Wikipedia-API (for Wikipedia parsing)
- Docker & Docker Compose (for containerization)
 
