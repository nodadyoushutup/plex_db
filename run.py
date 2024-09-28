import logging
import os

import coloredlogs
from flask_migrate import init, migrate, upgrade
from plexapi.server import PlexServer

from app.config import app, db, baseurl, token
from app.library import Library
from app.section import Section
from app.server import Server
from app.movie import Movie
from app.utils import download_image
from app.image import Image

# Set up the root logger
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)

coloredlogs.install(level="DEBUG")

# Ensure Flask, Alembic, and Werkzeug logs are propagated


def configure_loggers():
    for logger_name in ('flask.app', 'alembic.runtime.migration', 'werkzeug'):
        logger = logging.getLogger(logger_name)
        logger.setLevel(logging.DEBUG)
        logger.propagate = True


@app.route('/')
def index():
    return 'Welcome to the Library!'


plex = PlexServer(baseurl, token)


def ensure_migrations():
    """Ensure the database is migrated to the latest version."""
    migrations_path = os.path.join(os.path.dirname(__file__), 'migrations')
    if not os.path.exists(migrations_path):
        init()
    migrate()
    upgrade()


if __name__ == '__main__':
    with app.app_context():
        # ensure_migrations()
        configure_loggers()

        # server = Server.create(plex)

        # library = Library.create(plex.library)

        # print(vars(library))

        # # sections_data = plex.library.sections()
        # # for section in sections_data:
        # #     section = Section.create(section)

        movie_data = plex.library.sections()[0].getGuid(
            "plex://movie/5f40c0a086422500429b9877"
        )

        Movie.upsert(movie_data, _key="ratingKey")
        # movie = Movie.get({"ratingKey": 242031}, _first=True)
        # movie = Movie.search([("ratingKey", "=", 4), ("ratingKey", "=", 242031)], _first=True, _any=True)
        # print(movie.guids)

    app.run(
        debug=False
    )
