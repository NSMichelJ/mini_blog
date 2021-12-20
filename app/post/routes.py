from flask import Blueprint
from flask import render_template

from .models import Post

bp = Blueprint('post', __name__, template_folder='templates')

@bp.route('/article/<string:uuid>/<string:slug>')
def show_post(uuid, slug):
    post = Post.query.filter_by(public_id=uuid, title_slug=slug).first_or_404()
    return render_template('show_post.html', post=post)