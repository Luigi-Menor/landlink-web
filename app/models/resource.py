from .. import db
from datetime import datetime

class Recurso(db.Model):
    """Modelo para los recursos de una organización"""
    __tablename__ = 'recursos'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255), nullable=False)
    descripcion = db.Column(db.Text)
    tipo = db.Column(db.String(50))  # material, humano, financiero, etc.
    cantidad = db.Column(db.Integer)
    unidad = db.Column(db.String(50))  # unidades, horas, pesos, etc.
    estado = db.Column(db.String(50))  # disponible, en uso, agotado, etc.
    organizacion_id = db.Column(db.Integer, db.ForeignKey('organizaciones.id'), nullable=False)
    creado_en = db.Column(db.DateTime, default=datetime.utcnow)
    actualizado_en = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relaciones
    gestion = db.relationship('GestionRecursos', backref='recurso', lazy='dynamic')
    
    def __repr__(self):
        return f'<Recurso {self.nombre}>'


class GestionRecursos(db.Model):
    """Modelo para la gestión de recursos"""
    __tablename__ = 'gestion_recursos'
    
    id = db.Column(db.Integer, primary_key=True)
    recurso_id = db.Column(db.Integer, db.ForeignKey('recursos.id'), nullable=False)
    organizacion_id = db.Column(db.Integer, db.ForeignKey('organizaciones.id'), nullable=False)
    evento_id = db.Column(db.Integer, db.ForeignKey('eventos.id'))
    cantidad_asignada = db.Column(db.Integer)
    fecha_asignacion = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_devolucion = db.Column(db.DateTime)
    estado = db.Column(db.String(50))  # asignado, devuelto, perdido, etc.
    notas = db.Column(db.Text)
    
    def __repr__(self):
        return f'<GestionRecursos {self.id}>' 