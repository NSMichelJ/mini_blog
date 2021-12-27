from os.path import join

from flask import Blueprint
from flask import current_app
from flask import send_from_directory
from flask import render_template
from flask import request

from app.auth.models import User
from app.post.models import Post
from app.ext import db

bp = Blueprint('public', __name__, template_folder='templates')

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/search')
def search():
    q = request.args.get('q', '')
    results = Post.query.filter(Post.title.contains(q)).all()
    return render_template('search.html', results=results, q=q)

@bp.route('/user/<string:username>')
def show_user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('show_user.html', user=user)


@bp.route('/media/image/profile/<filename>')
def show_profile_image(filename):
    dir_path = join(
        current_app.config['MEDIA_DIR'],
        current_app.config['MEDIA_PROFILE_DIR']
    )
    return send_from_directory(dir_path, filename)

@bp.route('/media/thumbnail/profile/<filename>')
def show_profile_thumbnail(filename):
    dir_path = current_app.config['MEDIA_PROFILE_THUMBNAIL_DIR']
    return send_from_directory(dir_path, filename)

@bp.route('/media/image/background/<filename>')
def show_background_image(filename):
    dir_path = current_app.config['MEDIA_BACKGROUND_DIR']
    return send_from_directory(dir_path, filename)