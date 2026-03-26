from pydantic import BaseModel, Field
from app.schemas.episode import EpisodeResponse

class PodcastBase(BaseModel):
    title: str
    description: str | None = None
    youtube_channel_id: str

class PodcastCreate(PodcastBase):
    pass

class PodcastResponse(PodcastBase):
    id: int

    class Config:
        from_attributes = True

class PodcastWithEpisodes(PodcastResponse):
    episodes: list[EpisodeResponse] = Field(default_factory=list)