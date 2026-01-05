# Centralized application configuration loading environment variables from .env file
# python-dotenv, os

import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    if not SECRET_KEY:
        import warnings
        warnings.warn("SECRET_KEY not set! Using insecure default. Set SECRET_KEY environment variable for production!")
        SECRET_KEY = 'dev-only-insecure-key-change-in-production'
    
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    POKEMON_TCG_API_KEY = os.environ.get('POKEMON_TCG_API_KEY')
    
    if SQLALCHEMY_DATABASE_URI and SQLALCHEMY_DATABASE_URI.startswith("postgres://"):
        SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI.replace("postgres://", "postgresql://", 1)
        
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    WTF_CSRF_ENABLED = True
    WTF_CSRF_TIME_LIMIT = 3600
