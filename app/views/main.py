from flask import Blueprint, render_template
from ..models.event import Evento
from ..models.organization import Organizacion
from datetime import datetime

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """Página principal"""
    # Obtener eventos próximos
    proximos_eventos = Evento.query.filter(
        Evento.fecha >= datetime.utcnow().date()
    ).order_by(Evento.fecha).limit(6).all()
    
    # Obtener organizaciones destacadas
    organizaciones = Organizacion.query.limit(6).all()
    
    return render_template('main/index.html',
                         eventos=proximos_eventos,
                         organizaciones=organizaciones)

@main_bp.route('/about')
def about():
    """Página Acerca de"""
    return render_template('main/about.html')

@main_bp.route('/contact')
def contact():
    """Página de Contacto"""
    return render_template('main/contact.html') 