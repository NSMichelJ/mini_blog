"""
Utlidades de la app
"""

from flask import current_app, url_for
from itsdangerous import URLSafeTimedSerializer

def encode_token(email):
    """
    Retorna el email codificado.

    :param email:
        Dirección de email.
    """
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    return serializer.dumps(email, salt=current_app.config['SECURITY_PASSWORD_SALT'])

def decode_token(token, expiration=None):
    """
    Decodifica el token y retorna la dirección de email.

    :param token:
        Token a decodificar.
    :param expiration:
        Tiempo de expiración del token, default 3600s.
    """
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])

    if expiration is None:
        expiration = 3600

    try:
        email = serializer.loads(
            token,
            salt=current_app.config['SECURITY_PASSWORD_SALT'],
            max_age=expiration
        )
        return email
    except:
        return False
