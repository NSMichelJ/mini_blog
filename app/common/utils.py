"""
Utlidades de la app
"""

from flask import current_app
from itsdangerous import URLSafeTimedSerializer

def encode_token(obj):
    """
    Retorna un string codificado.

    :param obj:
        Tipo de dato a codificar
    """
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    return serializer.dumps(obj, salt=current_app.config['SECURITY_PASSWORD_SALT'])

def decode_token(token, expiration=None):
    """
    Decodifica el token y retorna un tipo de dato.

    :param token:
        Token a decodificar.
    :param expiration:
        Tiempo de expiración del token, default 3600s.
    """
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])

    if expiration is None:
        expiration = 3600

    try:
        obj = serializer.loads(
            token,
            salt=current_app.config['SECURITY_PASSWORD_SALT'],
            max_age=expiration
        )
        return obj

    except Exception:
        return False
