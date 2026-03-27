from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.services.chatbot import ask_chatbot
from app.db.session import get_db

router = APIRouter(prefix="/chat", tags=["Chatbot"])


class ChatRequest(BaseModel):
    message: str


@router.post("/")
def chat(request: ChatRequest, db: Session = Depends(get_db)):
    response = ask_chatbot(request.message, db)
    return {"response": response}