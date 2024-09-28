# relationship.py
from .movie import Movie
from .guid import Guid
from .config import db

Movie.guids = db.relationship(
    "Guid",
    back_populates="media",
    primaryjoin="and_(Guid.media_id==Movie.id, Guid.media_type=='movie')"
)
