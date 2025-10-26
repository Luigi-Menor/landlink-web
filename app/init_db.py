from app import db, create_app
from app.models.user import Role

def init_roles():
    """Inicializa los roles básicos del sistema"""
    app = create_app()
    with app.app_context():
        roles = [
            {
                'nombre': 'administrador',
                'descripcion': 'Administrador del sistema con acceso total'
            },
            {
                'nombre': 'organizador',
                'descripcion': 'Organizador de eventos y proyectos'
            },
            {
                'nombre': 'voluntario',
                'descripcion': 'Usuario voluntario'
            }
        ]
        
        for role_data in roles:
            role = Role.query.filter_by(nombre=role_data['nombre']).first()
            if not role:
                role = Role(**role_data)
                db.session.add(role)
        
        db.session.commit()

if __name__ == '__main__':
    init_roles() 