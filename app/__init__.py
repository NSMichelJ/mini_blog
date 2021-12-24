from decouple import config
from flask import Flask

from app.admin.routes import bp as admin_bp
from app.auth.routes import bp as auth_bp
from app.common.filters import strftime_filter
from app.dashboard.routes import bp as dash_bp
from app.ext import *
from app.post.routes import bp as post_bp
from app.public.routes import bp as public_bp

def create_app():
    """
    Crea y retorna la instancia de la app
    """
    settings_module = config('APP_SETTINGS_MODULE', default='config.default', cast=str)

    app = Flask(__name__)
    app.config.from_object(settings_module)

    register_filter(app)

    app.register_blueprint(public_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(dash_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(post_bp)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Por favor inicie sección'
    login_manager.login_message_category = 'info'
    csrf.init_app(app)
    ckeditor.init_app(app)
    mail.init_app(app)

    return app

def register_filter(app):
    """
    Registra los filtros de la app

    :param app:
        instancia de la app Flask
    """
    app.jinja_env.filters['strftime'] = strftime_filter
