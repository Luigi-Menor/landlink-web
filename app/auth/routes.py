from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.auth.jwt_auth import login_user, refresh_token, token_required, admin_required
from app.models.user import User

jwt_auth_bp = Blueprint('jwt_auth', __name__)

@jwt_auth_bp.route('/login', methods=['POST'])
def login():
    """Ruta para iniciar sesión y obtener tokens JWT"""
    data = request.get_json()
    
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({'message': 'Datos incompletos'}), 400
        
    result, error = login_user(data['email'], data['password'])
    
    if error:
        return jsonify({'message': error}), 401
        
    return jsonify(result), 200

@jwt_auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    """Ruta para refrescar el token de acceso"""
    return jsonify(refresh_token()), 200

@jwt_auth_bp.route('/me', methods=['GET'])
@token_required
def get_current_user():
    """Ruta para obtener información del usuario actual"""
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    return jsonify({
        'id': user.id,
        'email': user.correo_electronico,
        'nombre': user.get_full_name(),
        'rol': user.role.nombre
    }), 200

@jwt_auth_bp.route('/logout', methods=['POST'])
@token_required
def logout():
    """Ruta para cerrar sesión"""
    # En JWT, el logout se maneja en el cliente eliminando los tokens
    return jsonify({'message': 'Sesión cerrada exitosamente'}), 200 