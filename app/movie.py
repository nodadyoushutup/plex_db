# movie.py

from .config import db
from .model import Model
from .utils import build_url
from .image import Image
from app.guid import Guid


class Movie(Model):
    addedAt = db.Column(db.DateTime)
    art = db.Column(db.String)
    artBlurHash = db.Column(db.String)
    # fields = db.Column(db.JSON) # Relationship (future, do not touch)
    guid = db.Column(db.String)
    key = db.Column(db.String)
    lastRatedAt = db.Column(db.DateTime)
    lastViewedAt = db.Column(db.DateTime)
    librarySectionID = db.Column(db.Integer)
    librarySectionKey = db.Column(db.String)
    librarySectionTitle = db.Column(db.String)
    listType = db.Column(db.String)
    ratingKey = db.Column(db.Integer)
    summary = db.Column(db.Text)
    thumb = db.Column(db.String)
    thumbBlurHash = db.Column(db.String)
    title = db.Column(db.String)
    titleSort = db.Column(db.String)
    type = db.Column(db.String)
    userRating = db.Column(db.Float)
    viewCount = db.Column(db.Integer)
    playlistItemId = db.Column(db.Integer)
    playQueueItemId = db.Column(db.Integer)
    audienceRating = db.Column(db.Float)
    audienceRatingImage = db.Column(db.String)
    # chapters = db.Column(db.JSON) # Relationship (future, do not touch)
    chapterSource = db.Column(db.String)
    # collections = db.Column(db.JSON) # Relationship (future, do not touch)
    contentRating = db.Column(db.String)
    # countries = db.Column(db.JSON) # Relationship (future, do not touch)
    # directors = db.Column(db.JSON) # Relationship (future, do not touch)
    duration = db.Column(db.Integer)
    editionTitle = db.Column(db.String)
    enableCreditsMarkerGeneration = db.Column(db.Integer)
    # genres = db.Column(db.JSON) # Relationship (future, do not touch)
    # TODO: Make guids reverse relationship. This needs to be a many2many or
    # somehow allow you to find the media by doing guid.media_id or something to that effect
    guids = db.relationship(
        "Guid",
        primaryjoin="and_(foreign(Guid.media_id) == Movie.id, Guid.media_type == 'movie')",
        viewonly=True,
        backref="movie"
    )
    # labels = db.Column(db.JSON) # Relationship (future, do not touch)
    languageOverride = db.Column(db.String)
    # markers = db.Column(db.JSON) # Relationship (future, do not touch)
    # media = db.Column(db.JSON) # Relationship (future, do not touch)
    originallyAvailableAt = db.Column(db.DateTime)
    originalTitle = db.Column(db.String)
    primaryExtraKey = db.Column(db.String)
    # producers = db.Column(db.JSON) # Relationship (future, do not touch)
    rating = db.Column(db.Float)
    ratingImage = db.Column(db.String)
    # ratings = db.Column(db.JSON) # Relationship (future, do not touch)
    # roles = db.Column(db.JSON) # Relationship (future, do not touch)
    slug = db.Column(db.String)
    # similar = db.Column(db.JSON) # Relationship (future, do not touch)
    sourceURI = db.Column(db.String)
    studio = db.Column(db.String)
    tagline = db.Column(db.String)
    theme = db.Column(db.String)
    # ultraBlurColors = db.Column(db.JSON) # Relationship (future, do not touch)
    useOriginalTitle = db.Column(db.Integer)
    viewOffset = db.Column(db.Integer)
    # writers = db.Column(db.JSON) # Relationship (future, do not touch)
    year = db.Column(db.Integer)

    def download_images(self, force_ext=None, quality=None):
        self.download_thumb(force_ext, quality=quality)
        self.download_art(force_ext, quality=quality)

    def download_thumb(self, force_ext, quality=None):
        self._download_image("thumb", max_width=250,
                             force_ext=force_ext, quality=quality)

    def download_art(self, force_ext, quality=None):
        self._download_image("art", max_height=1080,
                             force_ext=force_ext, quality=quality)

    def _download_image(self, key, max_width=None, max_height=None, force_ext=None, quality=None):
        if key == "thumb":
            img_key = getattr(self, key)
            url = build_url(img_key)
        elif key == "art":
            img_key = getattr(self, key)
            url = build_url(img_key)
        else:
            raise ValueError(f"Unknown image key: {key}")
        image = Image(url, img_key)
        image.download(max_width, max_height, force_ext, quality=quality)

    @classmethod
    def upsert(cls, *args, _key="id", **kwargs):
        flattened_kwargs = cls._flatten_args_kwargs(*args, **kwargs)

        guids = flattened_kwargs.get("guids", [])
        obj_guids = []

        del flattened_kwargs["guids"]
        record = super().upsert(_key="ratingKey", **flattened_kwargs)

        for guid in guids:
            guid.guid = guid.id
            delattr(guid, "id")
            guid.media_id = record.id
            guid.media_type = "movie"
            obj_guids.append(Guid.upsert(guid, _key="guid"))

        record.guids.clear()
        record.guids.extend(obj_guids)
        db.session.commit()
        return record
