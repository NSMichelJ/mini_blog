from flask import Blueprint
from flask import render_template
from flask_login import login_required

from .decorators import admin_required

bp = Blueprint('admin', __name__, template_folder='templates')

@bp.route('/admin')
@login_required
@admin_required
def admin():
    return render_template('admin.html')