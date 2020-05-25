"""
------------------------------------------ Imports ------------------------------------------
"""
import os

from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy


"""
----------------------------------------- App Setup -----------------------------------------
"""
app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(12).hex()


"""
------------------------------------- DB Setup & Migrate ------------------------------------
"""
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///"+os.path.join(basedir, "data.sqlite")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app=app, db=db)


"""
---------------------------------------- Blueprints ------------------------------------------
"""
from radzblog.core.views import core


app.register_blueprint(core)