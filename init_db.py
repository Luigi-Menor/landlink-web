from app import create_app, db
from app.models.event import AreaIntervencion

def init_db():
    app = create_app()
    with app.app_context():
        # Crear áreas de intervención
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
            print("Base de datos inicializada exitosamente")
        except Exception as e:
            db.session.rollback()
            print(f"Error al inicializar la base de datos: {str(e)}")

if __name__ == '__main__':
    init_db() 