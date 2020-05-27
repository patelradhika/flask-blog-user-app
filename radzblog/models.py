"""
------------------------------------------ Imports ------------------------------------------
"""
from datetime import datetime
from flask_login import UserMixin
from radzblog import db, login_manager
from werkzeug.security import generate_password_hash,check_password_hash


"""
----------------------------------------- Load User -----------------------------------------
"""
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


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
    comments = db.relationship('Comment', backref='user', lazy=True)

    def __init__(self, email, username, password):
        self.email = email
        self.username = username
        self.password_hash = generate_password_hash(password)

    def __repr__(self):
        return f"User ID: {self.id} -- UserName: {self.username}"

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class BlogPost(db.Model):

    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140), nullable=False)
    content = db.Column(db.Text, nullable=False)
    written_on = db.Column(db.DateTime, nullable=False, default=datetime.now)
    posted = db.Column(db.Boolean, nullable=False, default=False)
    posted_on = db.Column(db.DateTime)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    comments = db.relationship('Comment', backref='post', lazy=True)

    def __init__(self, title, content, user_id):
        self.title = title
        self.content = content
        self.user_id =user_id


    def __repr__(self):
        return f"Title: {self.title} -- Written On: {self.written_on} -- Posted: {self.posted}"


class Comment(db.Model):

    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.Text, nullable=False)
    userid = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    postid = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)

    def __init__(self, comment, userid, postid):
        self.comment = comment
        self.userid = userid
        self.postid = postid

    def __repr__(self):
        return f"Comment: {self.comment} -- By User: {self.userid} -- On Post: {self.postid}"