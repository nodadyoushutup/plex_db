import pytest

from app.config import app, db


@pytest.fixture(scope='module')
def test_app():
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.testing = True

    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()
