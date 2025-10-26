from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from datetime import timedelta
import os

from .config import config

# Inicialización de extensiones
db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
jwt = JWTManager()
migrate = Migrate()
csrf = CSRFProtect()

# Configuración del login_manager
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Por favor inicie sesión para acceder a esta página.'
login_manager.login_message_category = 'info'

def create_app(config_name='default'):
    """Crea y configura la aplicación Flask"""
    app = Flask(__name__)
    
    # Cargar la configuración
    app.config.from_object(config[config_name])
    
    # Inicializar extensiones
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    csrf.init_app(app)
    
    # Registrar blueprints
    from .views.auth import auth_bp as views_auth_bp
    from .views.admin import admin_bp
    from .views.organizer import organizer_bp
    from .views.volunteer import volunteer_bp
    from .auth.routes import jwt_auth_bp
    
    app.register_blueprint(views_auth_bp)
    app.register_blueprint(jwt_auth_bp, url_prefix='/api/auth')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(organizer_bp, url_prefix='/organizer')
    app.register_blueprint(volunteer_bp, url_prefix='/volunteer')
    
    return app
