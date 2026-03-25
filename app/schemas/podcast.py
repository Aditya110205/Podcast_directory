from pydantic import BaseModel

class PodcastBase(BaseModel):
    title: str
    description: str | None = None
    youtube_channel_id: str

class PodcastCreate(PodcastBase):
    pass

class PodcastResponse(PodcastBase):
    id: int

    class Config:
        from_attributes = True   # for SQLAlchemy