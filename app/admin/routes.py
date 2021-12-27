from flask import Blueprint, current_app, render_template, request
from flask_login import login_required

from app.common.decorators import check_confirmed
from app.auth.models import User
from app.post.models import Post
from .decorators import admin_required

bp = Blueprint('admin', __name__, template_folder='templates')

@bp.route('/admin')
@login_required
@check_confirmed
@admin_required
def admin():
    return render_template('admin.html')

@bp.route('/admin/users')
@login_required
@check_confirmed
@admin_required
def show_users():
    page = request.args.get('page', 1, type=int)
    users = User.query.paginate(page, current_app.config['USER_PER_PAGE'])
    return render_template('show_users.html', users=users)

@bp.route('/admin/posts')
@login_required
@check_confirmed
@admin_required
def show_posts():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.paginate(page, current_app.config['POST_PER_PAGE'])
    return render_template('show_posts.html', posts=posts)
