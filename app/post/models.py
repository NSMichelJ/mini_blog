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
    comments = db.relationship('Comment',
        backref='post', lazy=True, cascade='all, delete-orphan',
        order_by='desc(Comment.id)')
    created = db.Column(db.DateTime, default=datetime.now())
    updated = db.Column(db.DateTime, nullable=True)

    def __init__(self, title, content, read_time, author_id):
        self.title = title
        self.content = content
        self.read_time = read_time
        self.author_id = author_id

    def __str__(self):
        return f'{self.title}'

    def save(self):
        self.title_slug = slugify(self.title)

        if not self.id:
            self.public_id = str(uuid4())
            db.session.add(self)
        else:
            self.updated = datetime.now()

        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

class Comment(db.Model):
    __tablename__ = 'comment'
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id', ondelete='CASCADE'), nullable=False)
    content = db.Column(db.Text)
    created = db.Column(db.DateTime, default=datetime.now())
    updated = db.Column(db.DateTime, nullable=True)

    def __init__(self, content, user_id, post_id):
        self.content = content
        self.user_id = user_id
        self.post_id = post_id

    def save(self):
        if not self.id:
            self.public_id = str(uuid4())
            db.session.add(self)
        else:
            self.updated = datetime.now()

        db.session.commit()
