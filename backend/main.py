from pathlib import Path
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from backend.models.ollama_client import OllamaClient
from backend.models.model_router import ModelRouter
from backend.models.model_manager import ModelManager
from backend.harness.agent import Agent


app = FastAPI(
    title="Sovereign AI Workbench",
    description="Local-first agentic AI workbench for confidential industrial work",
    version="0.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
         "http://localhost:5173",
         "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --------------------------------------------------
# Initialize model components
# --------------------------------------------------

model_router = ModelRouter()
model_manager = ModelManager()
agent = Agent()
UPLOAD_DIR = "inputs/uploads"



Path(UPLOAD_DIR).mkdir(
    parents=True,
    exist_ok=True
)


# --------------------------------------------------
# Request Model
# --------------------------------------------------

class ChatRequest(BaseModel):
    message: str
    task_type: str = "general"
    file_path: str 


# --------------------------------------------------
# Root
# --------------------------------------------------

@app.get("/")
def root():

    return {
        "system": "Sovereign AI Workbench",
        "status": "online",
        "mode": "local"
    }


# --------------------------------------------------
# Health Check
# --------------------------------------------------

@app.get("/health")
def health():

    return {
        "status": "healthy"
    }

@app.post("/upload")
async def upload_document(
    file: UploadFile = File(...)
):

    allowed_extensions = {
        ".pdf",
        ".png",
        ".jpg",
        ".jpeg",
        ".bmp",
        ".tiff",
        ".webp"
    }

    extension = Path(file.filename).suffix.lower()

    if extension not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type: {extension}"
        )

    file_path = Path(UPLOAD_DIR) / file.filename

    contents = await file.read()

    with open(file_path, "wb") as output_file:
        output_file.write(contents)

    return {
        "filename": file.filename,
        "file_path": str(file_path),
        "size": len(contents),
        "status": "uploaded"
    }


# --------------------------------------------------
# Chat
# --------------------------------------------------


@app.post("/chat")
def chat(request: ChatRequest):
        
    result = agent.run(
        task=request.message,
        file_path=request.file_path
    )

    return {
        "response": result.get("output"),
        "task": result.get("task"),
        "plan": result.get("plan"),
        "execution": result.get("execution"),
        "validation": result.get("validation"),

        # RAG sources
        "rag_sources": result.get("rag_sources", []),
        "analysis_sources": result.get("analysis_sources", []),
        "generation_sources": result.get("generation_sources", []),
        
        "execution_mode": "local"
    }




