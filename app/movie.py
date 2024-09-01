from datetime import datetime
from .config import db
from .model import Model
import os
import requests
from hashlib import md5

from .config import baseurl, token

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


    @classmethod
    def create(cls, obj=None, **kwargs):
        if obj is not None:
            def get_file_path_with_extension(url, path):
                response = requests.head(url)
                if response.status_code == 200:
                    content_type = response.headers['Content-Type']
                    extension = content_type.split('/')[-1]
                    return f"{path}.{extension}"
                return None

            def path_has_changed(current_path, new_path_with_extension):
                if not os.path.exists(current_path):
                    return True
                return os.path.basename(current_path) != os.path.basename(new_path_with_extension)

            def download_image(url, path):
                response = requests.get(url)
                if response.status_code == 200:
                    content_type = response.headers['Content-Type']
                    extension = content_type.split('/')[-1]
                    path_with_extension = f"{path}.{extension}"
                    with open(path_with_extension, 'wb') as file:
                        file.write(response.content)
                    cls.logger.info(f"Image saved to {path_with_extension}")
                else:
                    cls.logger.warning(f"Failed to download image from {url}")
            cls.logger.info(f"Synced movie: {obj.title} ({obj.year})")
            static_folder = os.path.join(os.path.dirname(__file__), '..', 'library')
            if obj.thumb:
                thumb_url = f"{baseurl}{obj.thumb}?X-Plex-Token={token}"
                thumb_path = os.path.join(static_folder, os.path.relpath(obj.thumb.replace("/library", ""), '/'))
                os.makedirs(os.path.dirname(thumb_path), exist_ok=True)
                thumb_path_with_extension = get_file_path_with_extension(thumb_url, thumb_path)
                if thumb_path_with_extension and path_has_changed(thumb_path_with_extension, thumb_path_with_extension):
                    download_image(thumb_url, thumb_path)
            if obj.art:
                art_url = f"{baseurl}{obj.art}?X-Plex-Token={token}"
                art_path = os.path.join(static_folder, os.path.relpath(obj.art.replace("/library", ""), '/'))
                os.makedirs(os.path.dirname(art_path), exist_ok=True)
                art_path_with_extension = get_file_path_with_extension(art_url, art_path)
                if art_path_with_extension and path_has_changed(art_path_with_extension, art_path_with_extension):
                    download_image(art_url, art_path)
        return super().create(obj=obj, **kwargs)