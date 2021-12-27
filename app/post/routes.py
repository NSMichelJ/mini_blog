from flask import Blueprint, current_app, redirect, \
                render_template, request, url_for
from flask_login import current_user, login_required

from app.common.decorators import check_confirmed
from .form import CommentForm
from .models import Comment
from .models import Post

bp = Blueprint('post', __name__, template_folder='templates')

@bp.route('/article/<string:uuid>/<string:slug>', methods=['GET', 'POST'])
def show_post(uuid, slug):
    post = Post.query.filter_by(public_id=uuid, title_slug=slug).first_or_404()
    form = CommentForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            comment = Comment(
                form.content.data,
                current_user.id,
                post.id
            )

            comment.save()
        return redirect(url_for('post.show_post',
            uuid=post.public_id,
            slug=post.title_slug
        ))
    return render_template('show_post.html', form=form, post=post)

@bp.route('/article/all')
def show_posts():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.id.desc()).paginate(page, current_app.config['POST_PER_PAGE'])
    return render_template('show_all_posts.html', posts=posts)

@bp.route('/like/<uuid>/<action>', methods=['GET'])
@login_required
@check_confirmed
def like_action(uuid, action):
    post = Post.query.filter_by(public_id=uuid).first_or_404()
    if action == 'like':
        current_user.like_post(post)
        current_user.save()
    if action == 'unlike':
        current_user.unlike_post(post)
        current_user.save()
    return redirect(request.referrer)
