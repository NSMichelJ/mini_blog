from flask import Blueprint
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from flask_login import login_user
from flask_login import current_user
from flask_login import logout_user
from flask_login import login_required
from werkzeug.urls import url_parse

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
                request.form['username'],
                request.form['first_name'],
                request.form['last_name'],
                request.form['email']
            )

            user.created_password(request.form['password'])
            user.save()

            login_user(user)
            return redirect(url_for('dashboard.dashboard'))

    return render_template('signup.html', form=form)

@bp.route('/logout')
def logout():
    if current_user.is_authenticated:
        logout_user()
    return redirect(url_for('public.index'))