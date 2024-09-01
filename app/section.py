# section.py

from app.movie import Movie
from .config import app, db
from .model import Model


class Section(Model):
    agent = db.Column(db.String)
    allow_sync = db.Column(db.Boolean)
    art = db.Column(db.String)
    composite = db.Column(db.String)
    filters = db.Column(db.Boolean)
    key = db.Column(db.Integer)
    language = db.Column(db.String)
    locations = db.Column(db.JSON)
    refreshing = db.Column(db.Boolean)
    scanner = db.Column(db.String)
    thumb = db.Column(db.String)
    title = db.Column(db.String)
    type = db.Column(db.String)
    
    @classmethod
    def create(cls, obj=None, **kwargs):
        if obj is not None:
            for media in obj.all():
                Movie.create(media) # This will change to work with other media types soon
        return super().create(obj=obj, **kwargs)