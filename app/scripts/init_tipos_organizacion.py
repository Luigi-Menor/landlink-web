from app import create_app, db
from app.models.organization import TipoOrganizacion

def init_tipos_organizacion():
    app = create_app()
    with app.app_context():
        # Verificar si ya existen tipos
        if TipoOrganizacion.query.count() == 0:
            tipos = [
                ('ONG', 'Organización No Gubernamental'),
                ('Colectivo', 'Grupo organizado de personas con objetivos comunes'),
                ('Junta de Acción Comunal', 'Organización comunitaria local'),
                ('Fundación', 'Entidad sin ánimo de lucro'),
                ('Asociación', 'Grupo de personas unidas para un fin común')
            ]
            
            for nombre, descripcion in tipos:
                tipo = TipoOrganizacion(nombre=nombre, descripcion=descripcion)
                db.session.add(tipo)
            
            try:
                db.session.commit()
                print("Tipos de organización creados exitosamente")
            except Exception as e:
                db.session.rollback()
                print(f"Error al crear tipos de organización: {str(e)}")
        else:
            print("Los tipos de organización ya existen")

if __name__ == '__main__':
    init_tipos_organizacion() 