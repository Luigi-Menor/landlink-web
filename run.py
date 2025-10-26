import os
from datetime import datetime
from app import create_app, db
from flask import g
from app.models.event import RolEvento
from app.utils.init_data import init_roles, create_admin_user

app = create_app(os.getenv('FLASK_CONFIG') or 'default')

@app.before_request
def before_request():
    """Ejecuta acciones antes de cada solicitud"""
    g.now = datetime.utcnow()

@app.context_processor
def inject_now():
    """Inyecta variables en todas las plantillas"""
    return {'now': datetime.utcnow()}

def init_db():
    """Inicializa la base de datos con datos básicos"""
    # Crear roles básicos y usuario administrador
    init_roles()
    create_admin_user()
    
    # Crear roles de evento
    roles_evento = ['Coordinador', 'Asistente', 'Logística', 'Comunicación', 'Facilitador']
    for rol in roles_evento:
        if not RolEvento.query.filter_by(nombre=rol).first():
            db.session.add(RolEvento(nombre=rol))
    
    db.session.commit()
    print('Base de datos inicializada con datos básicos')


    from flask import Flask

    app = Flask(__name__)

@app.route('/')
def test():
    return "✅ LandLink backend activo"

if __name__ == '__main__':
    with app.app_context():
        init_db()
    
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=5000)
