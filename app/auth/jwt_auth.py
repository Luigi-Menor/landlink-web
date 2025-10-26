from flask import jsonify, request
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity,
    get_jwt
)
from datetime import datetime, timedelta
from functools import wraps
from app.models.user import User
from app import db

def init_jwt_auth(app):
    """Inicializa la configuración JWT para la aplicación"""
    app.config['JWT_SECRET_KEY'] = app.config['JWT_SECRET_KEY']
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = app.config['JWT_ACCESS_TOKEN_EXPIRES']
    app.config['JWT_REFRESH_TOKEN_EXPIRES'] = app.config['JWT_REFRESH_TOKEN_EXPIRES']

def login_user(email, password):
    """Autentica un usuario y devuelve los tokens JWT"""
    user = User.query.filter_by(correo_electronico=email).first()
    
    if user and user.check_password(password):
        if not user.is_active():
            return None, "Usuario inactivo"
            
        # Crear tokens
        access_token = create_access_token(identity=user.id)
        refresh_token = create_refresh_token(identity=user.id)
        
        # Actualizar último login
        user.ultimo_intento_fallido = datetime.utcnow()
        db.session.commit()
        
        return {
            'access_token': access_token,
            'refresh_token': refresh_token,
            'user': {
                'id': user.id,
                'email': user.correo_electronico,
                'nombre': user.get_full_name(),
                'rol': user.role.nombre
            }
        }, None
    
    return None, "Credenciales inválidas"

def refresh_token():
    """Genera un nuevo token de acceso usando el token de actualización"""
    current_user_id = get_jwt_identity()
    access_token = create_access_token(identity=current_user_id)
    return {'access_token': access_token}

def token_required(f):
    """Decorador para proteger rutas que requieren autenticación"""
    @wraps(f)
    @jwt_required()
    def decorated(*args, **kwargs):
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user or not user.is_active():
            return jsonify({'message': 'Usuario no autorizado'}), 401
            
        return f(*args, **kwargs)
    return decorated

def admin_required(f):
    """Decorador para proteger rutas que requieren rol de administrador"""
    @wraps(f)
    @jwt_required()
    def decorated(*args, **kwargs):
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user or not user.is_active() or not user.is_admin():
            return jsonify({'message': 'Acceso denegado'}), 403
            
        return f(*args, **kwargs)
    return decorated 