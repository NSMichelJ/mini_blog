from flask import Blueprint
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