from datetime import datetime
from uuid import uuid4

from slugify import slugify

from app.ext import db

class Post(db.Model):
    __tablename__ = 'post'
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    title = db.Column(db.String)
    title_slug = db.Column(db.String)
    content = db.Column(db.Text)
    read_time = db.Column(db.Integer)
    created = db.Column(db.DateTime, default=datetime.now())
    updated = db.Column(db.String, nullable=True)

    def __init__(self, title, content, read_time, author_id):
        self.title = title
        self.content = content
        self.read_time = read_time
        self.author_id = author_id

    def __str__(self):
        return f'{self.title}'

    def save(self):
        self.title_slug = slugify(self.title)
        self.public_id = str(uuid4())
        db.session.add(self)
        db.session.commit()