from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.deps import get_db
from app.models.podcast import Podcast
from app.schemas.podcast import PodcastCreate, PodcastResponse

router = APIRouter(prefix="/podcasts", tags=["Podcasts"])


@router.post("/", response_model=PodcastResponse)
def create_podcast(podcast: PodcastCreate, db: Session = Depends(get_db)):
    db_podcast = Podcast(**podcast.dict())

    db.add(db_podcast)
    db.commit()
    db.refresh(db_podcast)

    return db_podcast


@router.get("/", response_model=list[PodcastResponse])
def get_podcasts(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    podcasts = db.query(Podcast).offset(skip).limit(limit).all()
    return podcasts