from fastapi import FastAPI, UploadFile, File
import os

from app.agents.document_agent import handle_document_query

from app.agents.meeting_agent import handle_meeting_query

from app.agents.weather_agent import get_weather_for_date
from datetime import date, timedelta
from app.schemas.chat_schema import ChatRequest
from app.agents.chat_router import route_query

from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse


app = FastAPI(title="Agentic AI Backend")

app.mount("/static", StaticFiles(directory="app/static"), name="static")

UPLOAD_DIR = "uploads"

@app.get("/")
def home():
    return FileResponse("app/static/index.html")

@app.post("/document/query")
def document_query(
    question: str,
    file: UploadFile = File(...)
):
    # Ensure upload directory exists
    os.makedirs(UPLOAD_DIR, exist_ok=True)

    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as f:
        f.write(file.file.read())

    response = handle_document_query(
        document_path=file_path,
        user_question=question
    )

    return {
        "agent": "document",
        "response": response
    }

@app.post("/document/upload")
def upload_document(file: UploadFile = File(...)):
    # Ensure upload directory exists
    os.makedirs(UPLOAD_DIR, exist_ok=True)

    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as f:
        f.write(file.file.read())
    
    return {
        "agent": "document",
        "response": f"File '{file.filename}' uploaded successfully."
    }

@app.post("/meeting/agent")
def meeting_agent(query: str):
    response = handle_meeting_query(query)
    return {
        "agent": "meeting",
        "response": response
    }
    

@app.post("/weather/agent")
def weather_agent(query: str):
    """
    Public API for Agent 1 (Weather Agent)
    """
    from app.agents.weather_agent import handle_weather_query
    return {
        "agent": "weather",
        "response": handle_weather_query(query)
    }
    

@app.post("/chat")
def chat(request: ChatRequest):
    return route_query(request.query)
