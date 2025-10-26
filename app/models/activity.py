from datetime import datetime
from .. import db

class HistorialActividad(db.Model):
    """Modelo para el historial de actividad de los voluntarios"""
    __tablename__ = 'historial_actividad'
    
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    evento_id = db.Column(db.Integer, db.ForeignKey('eventos.id'), nullable=False)
    fecha_participacion = db.Column(db.Date, nullable=False)
    rol_evento_id = db.Column(db.Integer, db.ForeignKey('roles_evento.id'))
    horas = db.Column(db.Integer)
    
    def __repr__(self):
        return f'<HistorialActividad {self.id}>'



