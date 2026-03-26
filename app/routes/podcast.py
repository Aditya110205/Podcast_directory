from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.deps import get_db
from app.models.podcast import Podcast
from app.schemas.podcast import PodcastCreate, PodcastResponse
from fastapi import HTTPException
from app.schemas.podcast import PodcastWithEpisodes
from app.services.youtube import fetch_channel_by_search, fetch_videos_by_channel
from app.models.episode import Episode

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

@router.get("/{podcast_id}", response_model=PodcastWithEpisodes)
def get_podcast(podcast_id: int, db: Session = Depends(get_db)):
    podcast = db.query(Podcast).filter(Podcast.id == podcast_id).first()

    if not podcast:
        raise HTTPException(status_code=404, detail="Podcast not found")

    return podcast

@router.post("/fetch/")
def fetch_and_store_podcast(query: str, db: Session = Depends(get_db)):
    
    channel = fetch_channel_by_search(query)

    if not channel:
        return {"error": "Channel not found"}

    # check if already exists
    existing = db.query(Podcast).filter(
        Podcast.youtube_channel_id == channel["channel_id"]
    ).first()

    if existing:
        return {"message": "Podcast already exists", "id": existing.id}

    # create podcast
    new_podcast = Podcast(
        title=channel["title"],
        description=channel["description"],
        youtube_channel_id=channel["channel_id"]
    )

    db.add(new_podcast)
    db.commit()
    db.refresh(new_podcast)

    # fetch episodes
    videos = fetch_videos_by_channel(channel["channel_id"])

    for video in videos:
        episode = Episode(
            title=video["title"],
            description=video["description"],
            youtube_video_id=video["video_id"],
            podcast_id=new_podcast.id
        )
        db.add(episode)

    db.commit()

    return {"message": "Podcast + episodes added", "podcast_id": new_podcast.id}