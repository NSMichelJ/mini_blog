"""
Configuración por defecto de la app
"""

from decouple import config

SECRET_KEY = 'SUPERMEGASECRET'
SECURITY_PASSWORD_SALT = 'SUPERMEGASECRET2'

SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db'
SQLALCHEMY_TRACK_MODIFICATIONS = False

CKEDITOR_SERVE_LOCAL = True
CKEDITOR_ENABLE_CODESNIPPET = True

MAIL_SERVER = config('MAIL_SERVER', default='smtp.gmail.com', cast=str)
MAIL_PORT = config('MAIL_PORT', default=587, cast=int)
MAIL_USE_TLS = config('MAIL_USE_TLS', default=True, cast=bool)
MAIL_USE_SSL = config('MAIL_USE_SSL', default=False, cast=bool)
MAIL_USERNAME = config('MAIL_USERNAME', cast=str)
MAIL_PASSWORD = config('MAIL_PASSWORD', cast=str)
MAIL_DEFAULT_SENDER = MAIL_USERNAME
