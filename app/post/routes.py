from flask import Blueprint
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from flask_login import current_user

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