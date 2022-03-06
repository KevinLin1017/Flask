from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first = db.Column(db.String(80), unique=False, nullable=True)
    last = db.Column(db.String(80), unique=False, nullable=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), unique=False, nullable=False)

    def __init__(self, first, last, email, password):
        self.first = first
        self.last = last
        self.email = email
        self.password = password


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first = db.Column(db.String(80), unique=False, nullable=True)
    title = db.Column(db.String(80), unique=False, nullable=True)
    post = db.Column(db.String(80), unique=False, nullable=True)

    def __init__(self, first, title, post):
        self.first = first
        self.title = title
        self.post = post
