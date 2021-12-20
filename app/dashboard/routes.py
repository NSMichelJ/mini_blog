from flask import Blueprint
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from flask_login import login_required
from flask_login import current_user

from app.post.models import Post
from .forms import WritePost

bp = Blueprint('dashboard', __name__, template_folder='templates')

@bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@bp.route('/dashboard/write-post', methods=['GET', 'POST'])
@login_required
def write_post():
    form = WritePost()
    if request.method == 'POST':
        if form.validate_on_submit:
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
