import re
from functools import wraps
from flask import abort, request, current_app
from flask_login import current_user
import jwt
from datetime import datetime, timedelta

def admin_required(f):
    """Decorador para requerir rol de administrador"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin():
            abort(403)
        return f(*args, **kwargs)
    return decorated_function

def organizer_required(f):
    """Decorador para requerir rol de organizador"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_organizer():
            abort(403)
        return f(*args, **kwargs)
    return decorated_function

def volunteer_required(f):
    """Decorador para requerir rol de voluntario"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_volunteer():
            abort(403)
        return f(*args, **kwargs)
    return decorated_function

def active_required(f):
    """Decorador para requerir que el usuario esté activo"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_active():
            abort(403)
        return f(*args, **kwargs)
    return decorated_function

def validate_password(password):
    """
    Valida que la contraseña cumpla con los requisitos de seguridad:
    - Al menos 8 caracteres
    - Al menos una letra mayúscula
    - Al menos una letra minúscula
    - Al menos un número
    - Al menos un carácter especial
    """
    if len(password) < 8:
        return False
    if not re.search(r'[A-Z]', password):
        return False
    if not re.search(r'[a-z]', password):
        return False
    if not re.search(r'[0-9]', password):
        return False
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return False
    return True

def generate_jwt_token(user_id, expiration=3600):
    """
    Genera un token JWT para el usuario
    """
    payload = {
        'exp': datetime.utcnow() + timedelta(seconds=expiration),
        'iat': datetime.utcnow(),
        'sub': user_id
    }
    return jwt.encode(
        payload,
        current_app.config.get('JWT_SECRET_KEY'),
        algorithm='HS256'
    )

def decode_jwt_token(token):
    """
    Decodifica un token JWT
    """
    try:
        payload = jwt.decode(
            token,
            current_app.config.get('JWT_SECRET_KEY'),
            algorithms=['HS256']
        )
        return payload['sub']
    except jwt.ExpiredSignatureError:
        return None  # Token expirado
    except jwt.InvalidTokenError:
        return None  # Token inválido

def sanitize_input(input_string):
    """
    Sanitiza una cadena de entrada para prevenir inyecciones
    """
    if input_string is None:
        return None
    # Eliminar caracteres potencialmente peligrosos
    sanitized = re.sub(r'[<>\'";]', '', input_string)
    return sanitized

def validate_request_origin():
    """
    Valida que la solicitud provenga de un origen permitido
    """
    origin = request.headers.get('Origin')
    if origin and origin in current_app.config.get('ALLOWED_ORIGINS', []):
        return True
    return False
