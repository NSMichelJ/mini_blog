from flask import Blueprint
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from flask_login import login_required
from flask_login import current_user

from app.post.models import Post
from .forms import WritePostForm

bp = Blueprint('dashboard', __name__, template_folder='templates')

@bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@bp.route('/dashboard/write-post', methods=['GET', 'POST'])
@login_required
def write_post():
    form = WritePostForm()
    if request.method == 'POST':
        if form.validate_on_submit:
            title = form.title.data
            content = form.content.data
            read_time = form.read_time.data

            post = Post(
                title,
                content,
                read_time,
                current_user.id
            )

            post.save()
            return redirect(url_for(
                'post.show_post',
                uuid=post.public_id,
                slug=post.title_slug
            ))
    return render_template('write_post.html', form=form)

@bp.route('/dashboard/<string:uuid>/edit-post', methods=['GET', 'POST'])
@login_required
def edit_post(uuid):
    post = Post.query.filter_by(public_id=uuid).first_or_404()

    form = WritePostForm(obj=post)
    if request.method == 'POST':
        if form.validate_on_submit:
            post.title = form.title.data
            post.content = form.content.data
            post.read_time = form.read_time.data

            post.save()

        return redirect(url_for(
                'post.show_post',
                uuid=post.public_id,
                slug=post.title_slug
            ))

    return render_template('edit_post.html', form=form)
