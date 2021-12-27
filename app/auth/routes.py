from datetime import datetime

from flask import Blueprint
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from flask import current_app
from flask_login import login_user
from flask_login import current_user
from flask_login import logout_user
from flask_login import login_required
from werkzeug.urls import url_parse

from app.common.mail import send_mail
from app.common.utils import encode_token, decode_token, save_image
from .forms import LoginForm
from .forms import SignupForm
from .forms import ResetPasswordForm
from .decorators import if_user_authenticated_redirect
from .models import User

bp = Blueprint('auth', __name__, template_folder='templates')

@bp.route('/login', methods=['GET', 'POST'])
@if_user_authenticated_redirect('dashboard.dashboard')
def login():
    form = LoginForm()
    
    if request.method == 'POST':
        username = form.username.data
        password = form.password.data

        user = User.query.filter_by(username=username).first()
        if user is not None and user.check_password(password):

            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')

            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('dashboard.dashboard')

            return redirect(next_page)

        flash('¡Usuario o Contraseña incorrecto!', 'danger')

    return render_template('login.html', form=form)

@bp.route('/signup', methods=['GET', 'POST'])
@if_user_authenticated_redirect('dashboard.dashboard')
def signup():
    form = SignupForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            user = User(
                form.username.data,
                form.first_name.data,
                form.last_name.data,
                form.email.data
            )

            user.created_password(form.password.data)

            if form.profile_image.data:
                user.profile_image_name = save_image(
                    form.profile_image.data,
                    current_app.config['MEDIA_PROFILE_DIR']
                )

            if form.background_image.data:
                user.background_image_name = save_image(
                    form.background_image.data,
                    current_app.config['MEDIA_BACKGROUND_DIR']
                )

            user.save()

            login_user(user)

            token = encode_token(user.email)
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
            flash('Un email de verificación fue enviado.', 'success')
            return redirect(url_for('auth.unconfirmed'))

    return render_template('signup.html', form=form)

@bp.route('/confirm/<token>', methods=['GET', 'POST'])
def confirm_email(token):
    email = decode_token(token)
    if not email:
        flash('El enlace de confirmación es invalido o a expirado.', 'danger')
        return redirect(url_for('auth.unconfirmed'))

    user = User.query.filter_by(email=email).first_or_404()

    if current_user.confirmed:
        flash('La cuenta ya esta confirmada.', 'success')
        return redirect(url_for('dashboard.dashboard'))

    user.confirmed = True
    user.confirmed_on = datetime.now()
    user.save()
    flash('Has confirmado tu cuenta. Gracias!', 'success')
    return redirect(url_for('dashboard.dashboard'))

@bp.route('/resend')
@login_required
def resend_confirmation():
    if not current_user.confirmed:
        token = encode_token(current_user.email)
        url = url = url_for('auth.confirm_email', token=token, _external=True)
        body = render_template('email_template/email.txt', url=url)
        html = render_template('email_template/email.html', url=url)
        send_mail(
            'Por favor, confirme su email',
            recipients=[current_user.email],
            sender=current_app.config['MAIL_USERNAME'],
            body=body,
            html=html
        )
        flash('Un nuevo email de confirmación ha sido enviado.', 'success')
        return redirect(url_for('auth.unconfirmed'))

    flash('La cuenta ya esta confirmada.', 'success')
    return redirect(url_for('dashboard.dashboard'))

@bp.route('/unconfirmed')
@login_required
def unconfirmed():
    if current_user.confirmed:
        flash('La cuenta ya esta confirmada.', 'success')
        return redirect(url_for('dashboard.dashboard'))
    return render_template('unconfirmed.html')

@bp.route('/reset_password', methods=['GET', 'POST'])
@if_user_authenticated_redirect('dashboard.dashboard')
def reset_password():
    form = ResetPasswordForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            email = form.email.data
            password = form.password.data
            obj = {
                'email': email,
                'password': password
            }

            token = encode_token(obj)
            url = url_for('auth.reset_with_token', token=token, _external=True)
            body = render_template('email_template/reset.txt', url=url)
            html = render_template('email_template/reset.html', url=url)
            send_mail(
                'Restablezca su contraseña',
                recipients=[email],
                sender=current_app.config['MAIL_USERNAME'],
                body=body,
                html=html
            )

            flash('Un email para restablecer su contraseña fue enviado', '')
            return redirect(url_for('public.index'))

    return render_template('reset_password.html', form=form)

@bp.route('/reset/<token>', methods=['GET', 'POST'])
@if_user_authenticated_redirect('dashboard.dashboard')
def reset_with_token(token):

    obj = decode_token(token)
    if not obj:
        flash('El enlace de restablecimiento es invalido o a expirado.', 'danger')
        return redirect(url_for('auth.unconfirmed'))

    user = User.query.filter_by(email=obj['email']).first_or_404()
    user.created_password(obj['password'])
    user.updated = datetime.now()
    user.save()
    flash('Has restablesido tu contraseña!', 'success')
    return redirect(url_for('auth.login'))

@bp.route('/logout')
def logout():
    if current_user.is_authenticated:
        logout_user()
    return redirect(url_for('public.index'))
