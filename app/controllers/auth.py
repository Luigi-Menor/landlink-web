from datetime import datetime, timedelta
from flask import current_app
from flask_login import login_user, logout_user, current_user
from .. import db, bcrypt
from ..models.user import User, Role, RegistroActividadUsuario
from ..utils.security import validate_password, generate_jwt_token
from ..utils.validators import validate_email

class AuthController:
    @staticmethod
    def register(data):
        """
        Registra un nuevo usuario
        """
        try:
            # Validar datos
            if not validate_email(data.get('correo_electronico')):
                return {'success': False, 'message': 'Correo electrónico inválido'}
            
            if not validate_password(data.get('contrasena')):
                return {'success': False, 'message': 'La contraseña no cumple con los requisitos de seguridad'}
            
            # Verificar si el correo ya está registrado
            existing_user = User.query.filter_by(correo_electronico=data.get('correo_electronico')).first()
            if existing_user:
                return {'success': False, 'message': 'El correo electrónico ya está registrado'}
            
            # Obtener el rol de voluntario (por defecto para nuevos usuarios)
            role = Role.query.filter_by(nombre='voluntario').first()
            if not role:
                # Si no existe, crearlo
                role = Role(nombre='voluntario', descripcion='Usuario voluntario')
                db.session.add(role)
                db.session.commit()
            
            # Procesar la fecha de nacimiento
            fecha_nacimiento = None
            if data.get('fecha_nacimiento'):
                try:
                    fecha_nacimiento = datetime.strptime(data.get('fecha_nacimiento'), '%Y-%m-%d').date()
                except ValueError:
                    return {'success': False, 'message': 'Formato de fecha de nacimiento inválido'}
            
            # Crear el nuevo usuario
            new_user = User(
                nombre=data.get('nombre'),
                apellido=data.get('apellido'),
                correo_electronico=data.get('correo_electronico'),
                telefono=data.get('telefono'),
                fecha_nacimiento=fecha_nacimiento,
                genero=data.get('genero'),
                rol_id=role.id,
                estado='activo'
            )
            
            # Establecer la contraseña
            new_user.contrasena = data.get('contrasena')
            
            # Guardar en la base de datos
            db.session.add(new_user)
            db.session.commit()
            
            # Registrar la actividad
            activity = RegistroActividadUsuario(
                usuario_id=new_user.id,
                accion='registro',
                detalles='Usuario registrado exitosamente'
            )
            db.session.add(activity)
            db.session.commit()
            
            return {'success': True, 'message': 'Usuario registrado exitosamente', 'user_id': new_user.id}
            
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f'Error en registro: {str(e)}')
            return {'success': False, 'message': 'Error al registrar el usuario. Por favor, inténtalo de nuevo.'}
    
    @staticmethod
    def login(email, password, remember=False):
        """
        Inicia sesión de un usuario
        """
        try:
            user = User.query.filter_by(correo_electronico=email).first()
            
            # Verificar si el usuario existe
            if not user:
                return {'success': False, 'message': 'Correo electrónico o contraseña incorrectos'}
            
            # Verificar si el usuario está bloqueado
            if user.estado == 'bloqueado':
                # Verificar si ha pasado el tiempo de bloqueo
                lockout_time = current_app.config.get('LOCKOUT_TIME', timedelta(minutes=15))
                if user.ultimo_intento_fallido and datetime.utcnow() - user.ultimo_intento_fallido > lockout_time:
                    # Desbloquear al usuario
                    user.estado = 'activo'
                    user.intentos_fallidos = 0
                    db.session.commit()
                else:
                    return {'success': False, 'message': 'Su cuenta está bloqueada. Intente más tarde.'}
            
            # Verificar si el usuario está inactivo
            if user.estado == 'inactivo':
                return {'success': False, 'message': 'Su cuenta está inactiva. Contacte al administrador.'}
            
            # Verificar la contraseña
            if not user.check_password(password):
                # Incrementar el contador de intentos fallidos
                user.intentos_fallidos += 1
                user.ultimo_intento_fallido = datetime.utcnow()
                
                # Bloquear al usuario si excede el número máximo de intentos
                max_attempts = current_app.config.get('MAX_LOGIN_ATTEMPTS', 5)
                if user.intentos_fallidos >= max_attempts:
                    user.estado = 'bloqueado'
                
                db.session.commit()
                
                return {'success': False, 'message': 'Correo electrónico o contraseña incorrectos'}
            
            # Resetear el contador de intentos fallidos
            user.intentos_fallidos = 0
            db.session.commit()
            
            # Iniciar sesión
            login_user(user, remember=remember)
            
            # Registrar la actividad
            activity = RegistroActividadUsuario(
                usuario_id=user.id,
                accion='login',
                detalles='Inicio de sesión exitoso'
            )
            db.session.add(activity)
            db.session.commit()
            
            # Generar token JWT para API
            token = generate_jwt_token(user.id)
            
            return {
                'success': True, 
                'message': 'Inicio de sesión exitoso',
                'user': {
                    'id': user.id,
                    'nombre': user.nombre,
                    'apellido': user.apellido,
                    'correo_electronico': user.correo_electronico,
                    'rol': user.role.nombre if user.role else None
                },
                'token': token
            }
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f'Error en login: {str(e)}')
            return {'success': False, 'message': 'Error al iniciar sesión. Por favor, inténtalo de nuevo.'}
    
    @staticmethod
    def logout():
        """
        Cierra la sesión del usuario actual
        """
        if current_user.is_authenticated:
            user_id = current_user.id
            
            # Registrar la actividad
            activity = RegistroActividadUsuario(
                usuario_id=user_id,
                accion='logout',
                detalles='Cierre de sesión exitoso'
            )
            db.session.add(activity)
            db.session.commit()
            
            # Cerrar sesión
            logout_user()
            
            return {'success': True, 'message': 'Cierre de sesión exitoso'}
        
        return {'success': False, 'message': 'No hay sesión activa'}
    
    @staticmethod
    def change_password(user_id, current_password, new_password):
        """
        Cambia la contraseña de un usuario
        """
        user = User.query.get(user_id)
        
        if not user:
            return {'success': False, 'message': 'Usuario no encontrado'}
        
        # Verificar la contraseña actual
        if not user.check_password(current_password):
            return {'success': False, 'message': 'Contraseña actual incorrecta'}
        
        # Validar la nueva contraseña
        if not validate_password(new_password):
            return {'success': False, 'message': 'La nueva contraseña no cumple con los requisitos de seguridad'}
        
        # Cambiar la contraseña
        user.contrasena = new_password
        db.session.commit()
        
        # Registrar la actividad
        activity = RegistroActividadUsuario(
            usuario_id=user.id,
            accion='cambio_contrasena',
            detalles='Cambio de contraseña exitoso'
        )
        db.session.add(activity)
        db.session.commit()
        
        return {'success': True, 'message': 'Contraseña cambiada exitosamente'}
    
    @staticmethod
    def request_password_reset(email):
        """
        Solicita un restablecimiento de contraseña
        """
        user = User.query.filter_by(correo_electronico=email).first()
        
        if not user:
            # Por seguridad, no revelar si el correo existe o no
            return {'success': True, 'message': 'Si el correo está registrado, recibirá instrucciones para restablecer su contraseña'}
        
        # Generar token de restablecimiento (válido por 1 hora)
        token = generate_jwt_token(user.id, expiration=3600)
        
        # Aquí se enviaría el correo con el enlace para restablecer la contraseña
        # Por simplicidad, solo devolvemos el token
        
        # Registrar la actividad
        activity = RegistroActividadUsuario(
            usuario_id=user.id,
            accion='solicitud_reset_contrasena',
            detalles='Solicitud de restablecimiento de contraseña'
        )
        db.session.add(activity)
        db.session.commit()
        
        return {
            'success': True, 
            'message': 'Si el correo está registrado, recibirá instrucciones para restablecer su contraseña',
            'token': token  # En producción, esto no se devolvería
        }
    
    @staticmethod
    def reset_password(token, new_password):
        """
        Restablece la contraseña de un usuario usando un token
        """
        from ..utils.security import decode_jwt_token
        
        # Decodificar el token
        user_id = decode_jwt_token(token)
        
        if not user_id:
            return {'success': False, 'message': 'Token inválido o expirado'}
        
        user = User.query.get(user_id)
        
        if not user:
            return {'success': False, 'message': 'Usuario no encontrado'}
        
        # Validar la nueva contraseña
        if not validate_password(new_password):
            return {'success': False, 'message': 'La nueva contraseña no cumple con los requisitos de seguridad'}
        
        # Cambiar la contraseña
        user.contrasena = new_password
        db.session.commit()
        
        # Registrar la actividad
        activity = RegistroActividadUsuario(
            usuario_id=user.id,
            accion='reset_contrasena',
            detalles='Restablecimiento de contraseña exitoso'
        )
        db.session.add(activity)
        db.session.commit()
        
        return {'success': True, 'message': 'Contraseña restablecida exitosamente'}
