from flask import Blueprint
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for

from app.ext import db
from .models import User

bp = Blueprint('auth', __name__, template_folder='templates')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':

        user = User.query.filter_by(username=request.form['username']).first()
        if user is not None and user.check_password(request.form['password']):
            return redirect(url_for('public.index'))

    return render_template('login.html')

@bp.route('/signup', methods=['GET', 'POST'])
def signup():
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
