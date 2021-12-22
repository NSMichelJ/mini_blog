from flask import Blueprint
from flask import render_template
from flask import request
from flask_login import login_required

from app.auth.models import User
from app.post.models import Post
from .decorators import admin_required

bp = Blueprint('admin', __name__, template_folder='templates')

@bp.route('/admin')
@login_required
@admin_required
def admin():
    return render_template('admin.html')

@bp.route('/admin/users')
@login_required
@admin_required
def show_users():
    users = User.query.all()
    return render_template('show_users.html', users=users)

@bp.route('/admin/posts')
@login_required
@admin_required
def show_posts():
    posts = Post.query.all()
    return render_template('show_posts.html', posts=posts)
