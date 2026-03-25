from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base

class Episode(Base):
    __tablename__ = "episodes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(String(500))
    youtube_video_id = Column(String(255), unique=True, index=True)

    podcast_id = Column(Integer, ForeignKey("podcasts.id"))

    podcast = relationship("Podcast", backref="episodes")