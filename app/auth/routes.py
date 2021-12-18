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

from app.ext import db
from .models import User

bp = Blueprint('auth', __name__, template_folder='templates')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.dashboard'))

    if request.method == 'POST':

        user = User.query.filter_by(username=request.form['username']).first()
        if user is not None and user.check_password(request.form['password']):
            # flash('¡Usuario o Contraseña incorrecto!', 'danger')

            login_user(user, remember=True)
            next_page = request.args.get('next')

            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('dashboard.dashboard')
            
            return redirect(next_page)
        else:
            flash('¡Usuario o Contraseña incorrecto!', 'danger')

    return render_template('login.html')

@bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.dashboard'))

    if request.method == 'POST':

        user = User(
            request.form['username'],
            request.form['first_name'],
            request.form['last_name'],
            request.form['email']
        )

        user.created_password(request.form['password'])
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('public.index'))

    return render_template('signup.html')

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('public.index'))