"""
Configuration settings for the Car Price Predictor application.
"""
import os
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).parent.parent

# Flask Configuration
class Config:
    """Base configuration class."""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    DEBUG = False
    TESTING = False
    
    # Model Configuration
    MODEL_PATH = BASE_DIR / 'models' / 'vehicle_price_model.pkl'
    DATA_PATH = BASE_DIR / 'CarPrice.csv'
    
    # API Configuration
    API_TITLE = 'Car Price Predictor API'
    API_VERSION = '1.0.0'
    API_DESCRIPTION = 'A machine learning API for predicting vehicle prices'
    
    # CORS Configuration
    CORS_ORIGINS = ['http://localhost:3000', 'http://127.0.0.1:5000']
    
    # Logging Configuration
    LOG_LEVEL = 'INFO'
    LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    LOG_LEVEL = 'DEBUG'

class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
    LOG_LEVEL = 'WARNING'

class TestingConfig(Config):
    """Testing configuration."""
    TESTING = True
    DEBUG = True

# Configuration mapping
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
