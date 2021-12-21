from datetime import datetime

from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash

from app.ext import db
from app.ext import login_manager

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)
    admin = db.Column(db.Boolean, default=False)
    posts = db.relationship('Post', backref='author', lazy=True, cascade="all, delete")
    comment = db.relationship('Comment', backref='author', lazy=True, cascade="all, delete")
    created = db.Column(db.DateTime, default=datetime.now())
    updated = db.Column(db.String, nullable=True)

    def __init__(self, username, first_name, last_name, email):
        self.username = username
        self.first_name = first_name
        self.last_name = last_name 
        self.email = email
    
    def __str__(self):
        return f'{self.username}'

    def created_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()

    def is_admin(self):
        return self.admin
    
    def create_admin(self):
        self.admin = True

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))