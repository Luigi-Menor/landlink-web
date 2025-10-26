import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from app import create_app, db
from app.models.event import AreaIntervencion

def init_areas_intervencion():
    app = create_app()
    with app.app_context():
        # Eliminar todas las áreas existentes
        AreaIntervencion.query.delete()
        
        areas = [
            ('Medio Ambiente', 'Actividades enfocadas en la protección y conservación del medio ambiente'),
            ('Educación', 'Proyectos educativos y de formación para la comunidad'),
            ('Salud', 'Iniciativas relacionadas con la salud y el bienestar comunitario'),
            ('Cultura', 'Actividades culturales y artísticas para el desarrollo comunitario'),
            ('Deporte', 'Eventos deportivos y recreativos para la comunidad'),
            ('Desarrollo Comunitario', 'Proyectos para el mejoramiento integral de la comunidad')
        ]
        
        for nombre, descripcion in areas:
            area = AreaIntervencion(nombre=nombre, descripcion=descripcion)
            db.session.add(area)
        
        try:
            db.session.commit()
            print("Áreas de intervención inicializadas exitosamente")
        except Exception as e:
            db.session.rollback()
            print(f"Error al inicializar áreas de intervención: {str(e)}")

if __name__ == '__main__':
    init_areas_intervencion() 