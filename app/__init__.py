import os

from flask import Flask

from app.public.routes import bp as public_bp
from app.auth.routes import bp as auth_bp
from app.ext import *

def create_app():
    settings_module = os.getenv('APP_SETTINGS_MODULE', default='config.default')
    
    app = Flask(__name__)
    app.config.from_object(settings_module)
    app.register_blueprint(public_bp)
    app.register_blueprint(auth_bp)

    db.init_app(app)
    migrate.init_app(app, db)

    return app
