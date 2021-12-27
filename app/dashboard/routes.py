from datetime import datetime

from flask import Blueprint
from flask import current_app
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from flask_login import login_required
from flask_login import current_user

from app.auth.models import User
from app.post.models import Post

from .forms import WritePostForm
from .forms import EditProfileForm
from app.common.decorators import check_confirmed
from app.common.utils import encode_token, save_image
from app.common.mail import send_mail

bp = Blueprint('dashboard', __name__, template_folder='templates')

@bp.route('/dashboard')
@login_required
@check_confirmed
def dashboard():
    return render_template('dashboard.html')

@bp.route('/dashboard/edit-profile', methods=['GET', 'POST'])
@login_required
@check_confirmed
def edit_profile():
    form = EditProfileForm(obj=current_user)
    if request.method == 'POST':
        if form.validate_on_submit():
            current_user.username = form.username.data
            current_user.first_name = form.first_name.data
            current_user.last_name = form.last_name.data

            if form.profile_image.data:
                print('XD 1')
                current_user.profile_image_name = save_image(
                    form.profile_image.data,
                    current_app.config['MEDIA_PROFILE_DIR']
                )
                current_user.profile_thumbnail = False

            if form.background_image.data:
                print('XD 2')
                current_user.background_image_name = save_image(
                    form.background_image.data,
                    current_app.config['MEDIA_BACKGROUND_DIR']
                )

            if form.password.data != '':
                current_user.created_password(form.password.data)

            if current_user.email != form.email.data:
                current_user.confirmed = False
                flash('Usted a cambiado su dirección de email, un email de verificación fue enviado.', 'warning')
                current_user.email= form.email.data

                token = encode_token(current_user.email)
                url = url_for('auth.confirm_email', token=token, _external=True)
                body = render_template('email_template/email.txt', url=url)
                html = render_template('email_template/email.html', url=url)
                send_mail(
                    'Por favor, confirme su email',
                    recipients=[current_user.email],
                    sender=current_app.config['MAIL_USERNAME'],
                    body=body,
                    html=html
                )

            flash('Perfil actualizado con exito', 'success')
            current_user.updated = datetime.now()
            current_user.save()
            return redirect(url_for('dashboard.dashboard'))

    return render_template('edit_profile.html', form=form)

@bp.route('/dashboard/write-post', methods=['GET', 'POST'])
@login_required
@check_confirmed
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
@check_confirmed
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

    return render_template('edit_post.html', form=form, post=post)

@bp.route('/dashboard/<string:uuid>/delete-post', methods=['GET', 'POST'])
@check_confirmed
@login_required
def delete_post(uuid):
    post = Post.query.filter_by(public_id=uuid).first_or_404()

    if post.author_id != current_user.id:
        return redirect(url_for('dashboard.dashboard'))

    if request.method == 'POST':
        post.delete()
        return redirect(url_for('dashboard.dashboard'))


    return render_template('delete_post.html', post=post)

@bp.route('/follow/<username>', methods=['POST'])
@login_required
@check_confirmed
def follow(username):
    if request.method == 'POST':
        user = User.query.filter_by(username=username).first_or_404()

        if user.id == current_user.id:
            return redirect(url_for('public.show_user', username=username))

        current_user.follow(user)
        current_user.save()
        return redirect(url_for('public.show_user', username=username))

@bp.route('/unfollow/<username>', methods=['POST'])
@login_required
@check_confirmed
def unfollow(username):
    if request.method == 'POST':
        user = User.query.filter_by(username=username).first_or_404()

        if user.id == current_user.id:
            return redirect(url_for('public.show_user', username=username))

        current_user.unfollow(user)
        current_user.save()
        return redirect(url_for('public.show_user', username=username))
