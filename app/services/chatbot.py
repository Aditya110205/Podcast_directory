from sqlalchemy.orm import Session
from app.models.podcast import Podcast
from app.core.config import settings
import requests


def ask_chatbot(message: str, db: Session):
    podcasts = db.query(Podcast).all()

    # 🔥 Filter based on user query
    filtered = [
        p for p in podcasts
        if message.lower() in p.title.lower()
    ]

    if filtered:
        podcast_list = "\n".join([f"- {p.title}" for p in filtered[:5]])
    else:
        podcast_list = "\n".join([f"- {p.title}" for p in podcasts[:5]])

    system_prompt = f"""
You are a smart podcast assistant.

Here are available podcasts:
{podcast_list}

Recommend podcasts based on user query.
"""