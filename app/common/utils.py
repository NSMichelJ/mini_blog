"""
Utlidades de la app
"""
from os import makedirs
from os.path import join
from threading import Thread
import uuid

from flask import current_app
from itsdangerous import URLSafeTimedSerializer
from werkzeug.utils import secure_filename

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

def save_image(file, path):
    image_name = str(uuid.uuid4()) + secure_filename(file.filename)
    media_dir = current_app.config['MEDIA_DIR']
    image_dir = join(media_dir, path)
    makedirs(image_dir, exist_ok=True)
    file_path = join(image_dir, image_name)
    file.save(file_path)
    return image_name
