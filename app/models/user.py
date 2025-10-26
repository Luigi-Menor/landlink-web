from datetime import datetime
from flask_login import UserMixin
from sqlalchemy.ext.hybrid import hybrid_property
from .. import db, bcrypt, login_manager

class Role(db.Model):
    """Modelo para los roles de usuario"""
    __tablename__ = 'roles'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255), unique=True, nullable=False)
    descripcion = db.Column(db.String(255))
    
    # Relaciones
    usuarios = db.relationship('User', backref='role', lazy='dynamic')
    
    def __repr__(self):
        return f'<Role {self.nombre}>'

class User(db.Model, UserMixin):
    """Modelo para los usuarios"""
    __tablename__ = 'usuarios'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255), nullable=False)
    apellido = db.Column(db.String(255), nullable=False)
    correo_electronico = db.Column(db.String(255), unique=True, nullable=False)
    telefono = db.Column(db.String(255))
    fecha_nacimiento = db.Column(db.Date)
    genero = db.Column(db.String(50))
    rol_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=False)
    _contrasena_hash = db.Column('contrasena_hash', db.String(255), nullable=False)
    estado = db.Column(db.String(50), default='activo')  # 'activo', 'inactivo', 'bloqueado'
    
    # Campos adicionales para seguridad
    intentos_fallidos = db.Column(db.Integer, default=0)
    ultimo_intento_fallido = db.Column(db.DateTime)
    
    # Relaciones
    actividades = db.relationship('RegistroActividadUsuario', backref='usuario', lazy='dynamic')
    solicitudes = db.relationship('SolicitudEvento', backref='usuario', lazy='dynamic')
    historial = db.relationship('HistorialActividad', backref='usuario', lazy='dynamic')
    comentarios = db.relationship('ComentarioCalificacion', backref='usuario', lazy='dynamic')
    
    # La relación con organizaciones se define en el modelo Organizacion
    
    @property
    def contrasena(self):
        raise AttributeError('La contraseña no es un atributo legible')
    
    @contrasena.setter
    def contrasena(self, password):
        """Establece el hash de la contraseña"""
        self._contrasena_hash = bcrypt.generate_password_hash(password).decode('utf-8')
    
    def check_password(self, password):
        """Verifica si la contraseña es correcta"""
        try:
            return bcrypt.check_password_hash(self._contrasena_hash, password)
        except Exception:
            return False
    
    def get_full_name(self):
        """Devuelve el nombre completo del usuario"""
        return f'{self.nombre} {self.apellido}'
    
    def is_admin(self):
        """Verifica si el usuario es administrador"""
        return self.role.nombre == 'administrador'
    
    def is_organizer(self):
        """Verifica si el usuario es organizador"""
        return self.role.nombre == 'organizador'
    
    def is_volunteer(self):
        """Verifica si el usuario es voluntario"""
        return self.role.nombre == 'voluntario'
    
    def is_active(self):
        """Verifica si el usuario está activo"""
        return self.estado == 'activo'
    
    def is_blocked(self):
        """Verifica si el usuario está bloqueado"""
        return self.estado == 'bloqueado'
    
    def __repr__(self):
        return f'<User {self.correo_electronico}>'


class RegistroActividadUsuario(db.Model):
    """Modelo para el registro de actividad de los usuarios"""
    __tablename__ = 'registro_actividad_usuario'
    
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'))
    accion = db.Column(db.String(255), nullable=False)
    detalles = db.Column(db.String(255))
    creado_en = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<RegistroActividadUsuario {self.id}>'


class HistorialCambiosUsuario(db.Model):
    """Modelo para el historial de cambios de los usuarios"""
    __tablename__ = 'historial_cambios_usuarios'
    
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    administrador_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    cambio = db.Column(db.String(255))
    fecha = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relaciones
    usuario = db.relationship('User', foreign_keys=[usuario_id], backref='cambios_recibidos')
    administrador = db.relationship('User', foreign_keys=[administrador_id], backref='cambios_realizados')
    
    def __repr__(self):
        return f'<HistorialCambiosUsuario {self.id}>'


@login_manager.user_loader
def load_user(user_id):
    """Carga un usuario desde la base de datos"""
    return User.query.get(int(user_id))
