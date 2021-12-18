from flask import Blueprint
from flask import render_template
from flask_login import login_required

bp = Blueprint('dashboard', __name__, template_folder='templates')

@bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')