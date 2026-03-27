from fastapi import FastAPI
from app.db.init_db import init_db
from app.routes import podcast
import threading
from app.services.background import background_fetch
from app.routes import ws

app = FastAPI()

@app.on_event("startup")
def on_startup():
    init_db()

app.include_router(podcast.router)

@app.get("/")
def read_root():
    return {"message": "Podcast API running 🚀"}

from app.routes import podcast, episode

app.include_router(podcast.router)
app.include_router(episode.router)


@app.on_event("startup")
def start_background_task():
    thread = threading.Thread(target=background_fetch, daemon=True)
    thread.start()

app.include_router(ws.router)

from app.routes import chat
app.include_router(chat.router)
