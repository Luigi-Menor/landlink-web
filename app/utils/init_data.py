from .. import db
from ..models.user import Role, User
from datetime import datetime

def init_roles():
    """Inicializa los roles básicos del sistema"""
    roles = [
        {
            'nombre': 'administrador',
            'descripcion': 'Administrador del sistema con acceso total'
        },
        {
            'nombre': 'organizador',
            'descripcion': 'Organizador de eventos'
        },
        {
            'nombre': 'voluntario',
            'descripcion': 'Voluntario que participa en eventos'
        }
    ]
    
    for rol_data in roles:
        if not Role.query.filter_by(nombre=rol_data['nombre']).first():
            rol = Role(**rol_data)
            db.session.add(rol)
    
    db.session.commit()

def create_admin_user():
    """Crea un usuario administrador por defecto"""
    # Verificar si ya existe un administrador
    admin_role = Role.query.filter_by(nombre='administrador').first()
    if not admin_role:
        init_roles()
        admin_role = Role.query.filter_by(nombre='administrador').first()
    
    # Verificar si ya existe el usuario admin
    if not User.query.filter_by(correo_electronico='admin@landlink.com').first():
        admin = User(
            nombre='Administrador',
            apellido='Sistema',
            correo_electronico='admin@landlink.com',
            rol_id=admin_role.id,
            estado='activo'
        )
        admin.contrasena = 'Admin123!'  # Contraseña por defecto
        db.session.add(admin)
        db.session.commit()
        print('Usuario administrador creado exitosamente')
    else:
        print('El usuario administrador ya existe') 