from fastapi import FastAPI
from app.db.init_db import init_db
from app.routes import podcast

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
