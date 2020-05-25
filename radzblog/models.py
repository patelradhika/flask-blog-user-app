"""
------------------------------------------ Imports ------------------------------------------
"""
from datetime import datetime
from flask_login import UserMixin
from radzblog import db
from werkzeug.security import generate_password_hash,check_password_hash


"""
------------------------------------------ Models -------------------------------------------
"""
class User(db.Model, UserMixin):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    profile_img = db.Column(db.String(20), nullable=False, default='default_profile.png')

    posts = db.relationship('BlogPost', backref='author', lazy=True)

    def __init__(self, email, username, password):
        self.email = email
        self.username = username
        self.password_hash = generate_password_hash(password)

    def __repr__(self):
        return f"User ID: {self.id} -- UserName: {self.username}"

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class BlogPost(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140), nullable=False)
    content = db.Column(db.Text, nullable=False)
    written_on = db.Column(db.DateTime, nullable=False, default=datetime.now)
    posted = db.Column(db.Boolean, nullable=False, default=False)
    posted_on = db.Column(db.DateTime)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __init__(self, title, content, user_id):
        self.title = title
        self.content = content
        self.user_id =user_id


    def __repr__(self):
        return f"Title: {self.title} -- Written On: {self.written_on} -- Posted: {self.posted}"