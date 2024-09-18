# config.py

from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
import os

baseurl = os.environ.get("BASEURL")
token = os.environ.get("TOKEN")
db_password = os.environ.get("DB_PASSWORD")
ip_address = os.environ.get("IP_ADDRESS")



static = "/home/ubuntu/plex_db/static"
app = Flask(__name__, static_folder=static)

# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://plex:{db_password}@{ip_address}:5432/plex"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['LOG_LEVEL'] = 'DEBUG'


db = SQLAlchemy(app)
migrate = Migrate(app, db)