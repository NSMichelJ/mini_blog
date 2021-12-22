from flask import Blueprint
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from flask_login import login_required
from flask_login import current_user

from app.post.models import Post
from .forms import WritePostForm
from .forms import EditProfileForm

bp = Blueprint('dashboard', __name__, template_folder='templates')

@bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@bp.route('/dashboard/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(obj=current_user)
    if request.method == 'POST':
        if form.validate_on_submit():
            current_user.username = form.username.data
            current_user.email = form.email.data
            current_user.first_name = form.first_name.data
            current_user.last_name = form.last_name.data

            current_user.save()

        return redirect(url_for('dashboard.dashboard'))
    return render_template('edit_profile.html', form=form)

@bp.route('/dashboard/write-post', methods=['GET', 'POST'])
@login_required
def write_post():
    form = WritePostForm()
    if request.method == 'POST':
        if form.validate_on_submit():
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
        if form.validate_on_submit():
            post.title = form.title.data
            post.content = form.content.data
            post.read_time = form.read_time.data

            if post.author_id == current_user.id:
                post.save()

        return redirect(url_for(
                'post.show_post',
                uuid=post.public_id,
                slug=post.title_slug
            ))

    return render_template('edit_post.html', form=form)

@bp.route('/dashboard/<string:uuid>/delete-post', methods=['GET', 'POST'])
@login_required
def delete_post(uuid):
    post = Post.query.filter_by(public_id=uuid).first_or_404()

    if post.author_id != current_user.id:
        return redirect(url_for('dashboard.dashboard'))

    if request.method == 'POST':
        post.delete()
        return redirect(url_for('dashboard.dashboard'))


    return render_template('delete_post.html', post=post)
