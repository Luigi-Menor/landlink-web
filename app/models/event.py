from datetime import datetime
from .. import db

class AreaIntervencion(db.Model):
    """Modelo para las áreas de intervención"""
    __tablename__ = 'areas_intervencion'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255), nullable=False)
    descripcion = db.Column(db.Text)
    
    # Relaciones
    eventos = db.relationship('Evento',
                            secondary='intervenciones_evento',
                            backref=db.backref('areas', lazy='dynamic'))
    
    def __repr__(self):
        return f'<AreaIntervencion {self.nombre}>'


class Evento(db.Model):
    """Modelo para los eventos"""
    __tablename__ = 'eventos'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255), nullable=False)
    fecha = db.Column(db.Date, nullable=False)
    descripcion = db.Column(db.String(255))
    ubicacion = db.Column(db.String(255))
    latitud = db.Column(db.Float(precision=9))
    longitud = db.Column(db.Float(precision=9))
    localidad = db.Column(db.String(255))
    organizacion_id = db.Column(db.Integer, db.ForeignKey('organizaciones.id'), nullable=False)
    requisitos = db.Column(db.Text)
    estado = db.Column(db.String(50), default='pendiente')  # pendiente, activo, cancelado, finalizado
    
    # Relaciones
    solicitudes = db.relationship('SolicitudEvento', backref='evento', lazy='dynamic')
    historial = db.relationship('HistorialActividad', backref='evento', lazy='dynamic')
    comentarios = db.relationship('ComentarioCalificacion', backref='evento', lazy='dynamic')
    recursos = db.relationship('GestionRecurso', backref='evento', lazy='dynamic')
    
    def __repr__(self):
        return f'<Evento {self.nombre}>'


# Tabla de asociación para la relación muchos a muchos entre eventos y áreas de intervención
intervenciones_evento = db.Table('intervenciones_evento',
    db.Column('evento_id', db.Integer, db.ForeignKey('eventos.id'), primary_key=True),
    db.Column('area_intervencion_id', db.Integer, db.ForeignKey('areas_intervencion.id'), primary_key=True)
)


class RolEvento(db.Model):
    """Modelo para los roles en eventos"""
    __tablename__ = 'roles_evento'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255), unique=True, nullable=False)
    
    # Relaciones
    actividades = db.relationship('HistorialActividad', backref='rol_evento', lazy='dynamic')
    
    def __repr__(self):
        return f'<RolEvento {self.nombre}>'


class SolicitudEvento(db.Model):
    """Modelo para las solicitudes de participación en eventos"""
    __tablename__ = 'solicitudes_evento'
    
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    evento_id = db.Column(db.Integer, db.ForeignKey('eventos.id'), nullable=False)
    estado = db.Column(db.String(50), default='pendiente')  # pendiente, aprobado, rechazado
    solicitado_en = db.Column(db.DateTime, default=datetime.utcnow)
    decidido_en = db.Column(db.DateTime)
    
    def __repr__(self):
        return f'<SolicitudEvento {self.id}>'


class GestionRecurso(db.Model):
    """Modelo para la gestión de recursos"""
    __tablename__ = 'gestion_recursos'
    
    id = db.Column(db.Integer, primary_key=True)
    evento_id = db.Column(db.Integer, db.ForeignKey('eventos.id'), nullable=False)
    nombre_recurso = db.Column(db.String(255), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    estado = db.Column(db.String(50))  # pendiente, aprobado, recibido, usado
    
    def __repr__(self):
        return f'<GestionRecurso {self.id}>'

class ComentarioCalificacion(db.Model):
    """Modelo para los comentarios y calificaciones de los eventos"""
    __tablename__ = 'comentarios_calificaciones'
    
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    evento_id = db.Column(db.Integer, db.ForeignKey('eventos.id'), nullable=False)
    comentario = db.Column(db.Text)
    calificacion = db.Column(db.Integer)
    creado_en = db.Column(db.DateTime, default=datetime.utcnow)
    
    __table_args__ = (
        db.UniqueConstraint('usuario_id', 'evento_id', name='unico_usuario_evento_comentario'),
    )