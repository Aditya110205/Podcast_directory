from sqlalchemy import Column, Integer, String
from app.db.base import Base

class Podcast(Base):
    __tablename__ = "podcasts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(String(500))
    youtube_channel_id = Column(String(255), unique=True, index=True)