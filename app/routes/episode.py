from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.deps import get_db
from app.models.episode import Episode
from app.schemas.episode import EpisodeCreate, EpisodeResponse

router = APIRouter(prefix="/episodes", tags=["Episodes"])

@router.post("/", response_model=EpisodeResponse)
def create_episode(episode: EpisodeCreate, db: Session = Depends(get_db)):
    db_episode = Episode(**episode.dict())

    db.add(db_episode)
    db.commit()
    db.refresh(db_episode)

    return db_episode

@router.get("/{podcast_id}", response_model=list[EpisodeResponse])
def get_episodes(podcast_id: int, db: Session = Depends(get_db)):
    episodes = db.query(Episode).filter(Episode.podcast_id == podcast_id).all()
    return episodes

@router.get("/search/", response_model=list[EpisodeResponse])
def search_episodes(query: str, db: Session = Depends(get_db)):
    episodes = db.query(Episode).filter(Episode.title.ilike(f"%{query}%")).all()
    return episodes