# guid.py
from .config import db
from .model import Model


class Guid(Model):
    id = db.Column(db.Integer, primary_key=True)
    guid = db.Column(db.String)
    media_type = db.Column(db.String)
    media_id = db.Column(db.Integer)
    __table_args__ = (
        db.CheckConstraint(
            "(media_type = 'movie' AND media_id IS NOT NULL) OR "
            "(media_type = 'episode' AND media_id IS NOT NULL)"
        ),
    )
