from datetime import datetime
from .config import db
from .model import Model
from hashlib import md5
from .utils import build_url
from .image import Image


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
    # guids = db.Column(db.JSON) # Relationship (future, do not touch)
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
        self._download_image("thumb", max_width=250, force_ext=force_ext, quality=quality)

    def download_art(self, force_ext, quality=None):
        self._download_image("art", max_height=1080, force_ext=force_ext, quality=quality)

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
    def create(cls, _obj=None, **kwargs):
        record = super().create(_obj, **kwargs)
        # record.download_images(force_ext="jpg", quality=50)
        return record