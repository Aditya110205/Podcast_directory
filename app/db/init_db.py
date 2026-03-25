from app.db.base import Base
from app.db.session import engine

# import models (IMPORTANT)
from app.models.podcast import Podcast
from app.models.episode import Episode

def init_db():
    Base.metadata.create_all(bind=engine)