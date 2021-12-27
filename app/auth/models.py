from os import makedirs
from os.path import join
from datetime import datetime

from flask import current_app, url_for
from flask_login import UserMixin
from PIL import Image
from werkzeug.security import check_password_hash, generate_password_hash

from app.ext import db, login_manager
from app.post.models import PostLike

followers = db.Table('followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
)

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)
    admin = db.Column(db.Boolean, default=False)
    background_image_name = db.Column(db.String)
    profile_image_name = db.Column(db.String, default='')
    profile_thumbnail = db.Column(db.Boolean, default=False)
    posts = db.relationship('Post',
        backref='author', lazy=True,
        cascade="all, delete", order_by='desc(Post.id)'
    )
    comment = db.relationship('Comment', backref='author', lazy=True, cascade="all, delete")
    confirmed = db.Column(db.Boolean, default=False)
    confirmed_on = db.Column(db.DateTime, nullable=True)
    created = db.Column(db.DateTime, default=datetime.now())
    updated = db.Column(db.DateTime, nullable=True)
    followed = db.relationship(
        'User', secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref('followers', lazy='dynamic'), lazy='dynamic')
    liked = db.relationship(
        'PostLike',
        foreign_keys='PostLike.user_id',
        backref='user', lazy='dynamic')

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

    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)

    def is_following(self, user):
        return self.followed.filter(
            followers.c.followed_id == user.id).count() > 0

    def like_post(self, post):
        if not self.has_liked_post(post):
            like = PostLike(user_id=self.id, post_id=post.id)
            db.session.add(like)

    def unlike_post(self, post):
        if self.has_liked_post(post):
            PostLike.query.filter_by(
                user_id=self.id,
                post_id=post.id).delete()

    def has_liked_post(self, post):
        return PostLike.query.filter(
            PostLike.user_id == self.id,
            PostLike.post_id == post.id).count() > 0

    def get_thumbnail(self):
        if self.profile_image_name and not self.profile_thumbnail:
            pathname = join(
                current_app.config['MEDIA_PROFILE_DIR'],
                self.profile_image_name
            )

            makedirs(current_app.config['MEDIA_PROFILE_THUMBNAIL_DIR'], exist_ok=True)

            with Image.open(pathname) as img:
                img.resize((250, 250))
                outfile = join(
                    current_app.config['MEDIA_PROFILE_THUMBNAIL_DIR'],
                    self.profile_image_name
                )
                img.save(outfile, "JPEG")

            self.profile_thumbnail = True
            self.save()

            return url_for('public.show_profile_thumbnail', filename=self.profile_image_name)

        elif self.profile_image_name:
            return url_for('public.show_profile_thumbnail', filename=self.profile_image_name)

        else:
            return ''

    def get_background(self):
        if self.background_image_name is not None:
            url = url_for('public.show_background_image', filename=self.background_image_name)
            return url
        else:
            return ''

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))
