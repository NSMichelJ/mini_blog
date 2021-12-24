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
from app.common.utils import encode_token, decode_token
from .forms import LoginForm
from .forms import SignupForm
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
        else:
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

            user.created_password(request.form['password'])
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
            return redirect(url_for('auth.unconfirmed'))

    return render_template('signup.html', form=form)

@bp.route('/confirm/<token>')
@login_required
def confirm_email(token):
    if current_user.confirmed:
        flash('La cuenta ya esta confirmada.', 'success')
    else:
        try:
            email = decode_token(token)
        except:
            flash('El enlace de confirmación es invalido o a expirado.', 'danger')
        user = User.query.filter_by(email=email).first_or_404()

        user.confirmed = True
        user.confirmed_on = datetime.now()
        user.save()
        flash('Has confirmado tu email. Gracias!', 'success')
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
    else:
        flash('La cuenta ya esta confirmada.', 'success')
        return redirect(url_for('dashboard.dashboard'))

@bp.route('/unconfirmed')
@login_required
def unconfirmed():
    if current_user.confirmed:
        flash('La cuenta ya esta confirmada.', 'success')
        return redirect(url_for('dashboard.dashboard'))
    return render_template('unconfirmed.html')

@bp.route('/logout')
def logout():
    if current_user.is_authenticated:
        logout_user()
    return redirect(url_for('public.index'))