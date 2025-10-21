"""Database configuration for Surfshark VPN Analytics"""
import os
from pathlib import Path

class AppConfig:
    """Application configuration"""
    
    # Get the base directory (project root)
    BASE_DIR = Path(__file__).parent.parent.parent
    
    # Database configuration
    # SQLite absolute path requires 4 slashes: sqlite:////absolute/path
    # The extra slash comes from the leading / in the absolute path
    DB_PATH = str(BASE_DIR.absolute() / 'instance' / 'surfshark_vpn.db')
    _default_uri = f'sqlite:///{DB_PATH}'
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', _default_uri)
    
    # Debug: Print what we're using
    print(f"[CONFIG] DB_PATH: {DB_PATH}")
    print(f"[CONFIG] DATABASE_URI: {SQLALCHEMY_DATABASE_URI}")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False
    
    # Flask configuration
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    DEBUG = os.getenv('FLASK_DEBUG', '1') == '1'
    
    # API configuration
    API_PORT = int(os.getenv('API_PORT', 5002))
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', 'http://localhost:3000').split(',')