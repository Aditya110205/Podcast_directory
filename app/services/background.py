import time
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.db.session import SessionLocal
from app.models.podcast import Podcast
from app.models.episode import Episode
from app.services.youtube import fetch_videos_by_channel
from app.services.ws_manager import manager
import asyncio


def background_fetch():
    while True:
        print("🔄 Checking for new episodes...")

        db: Session = SessionLocal()

        podcasts = db.query(Podcast).all()

        for podcast in podcasts:
            videos = fetch_videos_by_channel(podcast.youtube_channel_id)  # ✅ IMPORTANT

            for video in videos:
                try:
                    new_episode = Episode(
                        title=video["title"],
                        description=video["description"],
                        youtube_video_id=video["video_id"],
                        podcast_id=podcast.id
                    )
                    db.add(new_episode)
                    db.commit()

                    print(f"✅ New episode added: {video['title']}")
                    asyncio.run(manager.broadcast(f"New episode: {video['title']}"))

                except IntegrityError:
                    db.rollback()
                    print(f"⚠️ Duplicate skipped: {video['video_id']}")

        db.close()
        time.sleep(60)