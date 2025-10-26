import os
from datetime import timedelta

class Config:
    """Configuración base para la aplicación"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'clave-secreta-por-defecto-cambiar-en-produccion'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'mssql+pyodbc://Luigi:123@localhost/landlink1?driver=ODBC+Driver+18+for+SQL+Server&TrustServerCertificate=yes&Encrypt=yes'
    
    # Configuración de JWT
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'jwt-clave-secreta-por-defecto-cambiar-en-produccion'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    
    # Configuración de seguridad
    BCRYPT_LOG_ROUNDS = 12
    MAX_LOGIN_ATTEMPTS = 5
    LOCKOUT_TIME = timedelta(minutes=15)
    
    # Configuración de la aplicación
    ITEMS_PER_PAGE = 10
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static/uploads')
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf', 'doc', 'docx'}
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB
    
    # Configuración de cookies
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    PERMANENT_SESSION_LIFETIME = timedelta(hours=1)
    REMEMBER_COOKIE_DURATION = timedelta(days=1)
    REMEMBER_COOKIE_SECURE = True
    REMEMBER_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_SAMESITE = 'Lax'

class DevelopmentConfig(Config):
    """Configuración para desarrollo"""
    DEBUG = True
    SQLALCHEMY_ECHO = True
    SESSION_COOKIE_SECURE = False
    REMEMBER_COOKIE_SECURE = False

class TestingConfig(Config):
    """Configuración para pruebas"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False
    SESSION_COOKIE_SECURE = False
    REMEMBER_COOKIE_SECURE = False

class ProductionConfig(Config):
    """Configuración para producción"""
    DEBUG = False
    
    # En producción, asegúrate de que estas variables de entorno estén configuradas
    SECRET_KEY = os.environ.get('SECRET_KEY')
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
