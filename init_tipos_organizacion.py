from app import create_app, db
from app.models.organization import TipoOrganizacion

def init_tipos_organizacion():
    app = create_app()
    with app.app_context():
        # Crear tipos de organización
        tipos = [
            ('ONG', 'Organización No Gubernamental'),
            ('Fundación', 'Fundación sin ánimo de lucro'),
            ('Asociación', 'Asociación comunitaria'),
            ('Cooperativa', 'Cooperativa de trabajo'),
            ('Empresa Social', 'Empresa con enfoque social'),
            ('Institución Educativa', 'Centro educativo o universidad'),
            ('Gobierno Local', 'Entidad gubernamental local'),
            ('Grupo Comunitario', 'Grupo organizado de la comunidad')
        ]
        
        for nombre, descripcion in tipos:
            tipo = TipoOrganizacion(nombre=nombre, descripcion=descripcion)
            db.session.add(tipo)
        
        try:
            db.session.commit()
            print("Tipos de organización inicializados exitosamente")
        except Exception as e:
            db.session.rollback()
            print(f"Error al inicializar los tipos de organización: {str(e)}")

if __name__ == '__main__':
    init_tipos_organizacion() 