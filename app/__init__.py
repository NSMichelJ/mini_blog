from flask import Flask

from app.public.routes import bp as public_bp

def create_app():
    app = Flask(__name__)
    app.register_blueprint(public_bp)
    return app
