from flask import Blueprint
from flask import render_template

from app.auth.models import User

bp = Blueprint('public', __name__, template_folder='templates')

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/user/<string:username>')
def show_user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('show_user.html', user=user)