import os

from flask import Flask

from app.admin.routes import bp as admin_bp 
from app.auth.routes import bp as auth_bp
from app.dashboard.routes import bp as dash_bp
from app.ext import *
from app.public.routes import bp as public_bp

def create_app():
    settings_module = os.getenv('APP_SETTINGS_MODULE', default='config.default')
    
    app = Flask(__name__)
    app.config.from_object(settings_module)
    app.register_blueprint(public_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(dash_bp)
    app.register_blueprint(admin_bp)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Por favor inicie sección'
    login_manager.login_message_category = 'info'
    csrf.init_app(app)

    return app
