from pydantic import BaseModel

class EpisodeBase(BaseModel):
    title: str
    description: str | None = None
    youtube_video_id: str
    podcast_id: int

class EpisodeCreate(EpisodeBase):
    pass

class EpisodeResponse(EpisodeBase):
    id: int

    class Config:
        from_attributes = True