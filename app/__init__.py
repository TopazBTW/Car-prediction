"""
Car Price Predictor Flask Application Factory.
"""
from flask import Flask
from flask_cors import CORS
from config.settings import config
from app.api.routes import api_bp, init_model_manager
from app.utils.logger import get_logger

logger = get_logger(__name__)

def create_app(config_name='default'):
    """
    Create and configure the Flask application.
    
    Args:
        config_name: Configuration name ('development', 'production', 'testing')
        
    Returns:
        Configured Flask application
    """
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config[config_name])
    
    # Initialize CORS
    CORS(app, origins=app.config.get('CORS_ORIGINS', ['*']))
    
    # Register blueprints
    app.register_blueprint(api_bp)
    
    # Initialize model manager
    with app.app_context():
        try:
            init_model_manager()
            logger.info("Application initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize application: {e}")
            raise
    
    return app
