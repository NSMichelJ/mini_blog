from flask import Blueprint
from flask import render_template

bp = Blueprint('public', __name__, template_folder='templates')

@bp.route('/')
def index():
    return render_template('index.html')
