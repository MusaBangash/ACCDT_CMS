"""
Application configuration for development, testing, and production environments.
"""

import os
from datetime import timedelta


class Config:
    """Base configuration - common to all environments"""
    
    # Flask
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    REMEMBER_COOKIE_DURATION = timedelta(days=7)
    SESSION_COOKIE_SECURE = False  # Set to True in production with HTTPS
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # File uploads
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER') or 'app/static/uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif', 'pdf'}
    
    # Pagination
    ITEMS_PER_PAGE = 10
    
    # Database
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    """Development configuration - SQLite"""
    
    DEBUG = True
    TESTING = False
    
    # SQLite for development (no additional setup needed)
    basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        f'sqlite:///{os.path.join(basedir, "school_dev.db")}'
    
    # Disable CSRF in development (not recommended in production)
    WTF_CSRF_ENABLED = True


class TestingConfig(Config):
    """Testing configuration - In-memory SQLite"""
    
    DEBUG = True
    TESTING = True
    
    # In-memory SQLite for testing
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False


class ProductionConfig(Config):
    """Production configuration - PostgreSQL"""
    
    DEBUG = False
    TESTING = False
    
    # PostgreSQL for production
    # Example: postgresql://user:password@localhost/school_db
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'postgresql://user:password@localhost/school_db'
    
    # Security settings
    SESSION_COOKIE_SECURE = True
    WTF_CSRF_ENABLED = True


# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}


def get_config(config_name=None):
    """Get configuration based on environment"""
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')
    return config.get(config_name, config['default'])
