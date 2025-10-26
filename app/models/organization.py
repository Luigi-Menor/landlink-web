from .. import db
from datetime import datetime

class TipoOrganizacion(db.Model):
    """Modelo para los tipos de organización"""
    __tablename__ = 'tipos_organizacion'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255), unique=True, nullable=False)
    descripcion = db.Column(db.Text)
    
    # Relaciones
    organizaciones = db.relationship('Organizacion', backref='tipo_organizacion', lazy='dynamic')
    
    def __repr__(self):
        return f'<TipoOrganizacion {self.nombre}>'


class Organizacion(db.Model):
    """Modelo para las organizaciones"""
    __tablename__ = 'organizaciones'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255), nullable=False)
    tipo_organizacion_id = db.Column(db.Integer, db.ForeignKey('tipos_organizacion.id'), nullable=False)
    localidad = db.Column(db.String(255))
    descripcion = db.Column(db.Text)
    correo_electronico = db.Column(db.String(255))
    telefono = db.Column(db.String(255))
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relaciones
    eventos = db.relationship('Evento', backref='organizacion', lazy='dynamic')
    
    # Relación con usuarios (organizadores)
    usuarios = db.relationship('User',
                           secondary='organizadores',
                           backref=db.backref('organizaciones', lazy='dynamic'))
    
    # Relación con áreas de trabajo
    areas_trabajo = db.relationship('AreaIntervencion',
                                 secondary='organizaciones_areas',
                                 backref=db.backref('organizaciones', lazy='dynamic'))
    
    def __repr__(self):
        return f'<Organizacion {self.nombre}>'


# Tabla de asociación para la relación muchos a muchos entre usuarios y organizaciones
organizadores = db.Table('organizadores',
    db.Column('usuario_id', db.Integer, db.ForeignKey('usuarios.id'), primary_key=True),
    db.Column('organizacion_id', db.Integer, db.ForeignKey('organizaciones.id'), primary_key=True)
)

# Tabla de asociación para la relación muchos a muchos entre organizaciones y áreas de trabajo
organizaciones_areas = db.Table('organizaciones_areas',
    db.Column('organizacion_id', db.Integer, db.ForeignKey('organizaciones.id'), primary_key=True),
    db.Column('area_id', db.Integer, db.ForeignKey('areas_intervencion.id'), primary_key=True)
)
