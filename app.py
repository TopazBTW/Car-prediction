"""
Main application entry point for the Car Price Predictor.
"""
import os
from app import create_app
from app.utils.logger import get_logger

logger = get_logger(__name__)

def main():
    """Main application entry point."""
    # Get configuration from environment
    config_name = os.environ.get('FLASK_ENV', 'development')
    
    # Create application
    app = create_app(config_name)
    
    # Get configuration
    host = os.environ.get('HOST', '0.0.0.0')
    port = int(os.environ.get('PORT', 5000))
    debug = app.config.get('DEBUG', False)
    
    logger.info(f"Starting Car Price Predictor API on {host}:{port}")
    logger.info(f"Configuration: {config_name}")
    logger.info(f"Debug mode: {debug}")
    
    # Run application
    app.run(
        host=host,
        port=port,
        debug=debug,
        threaded=True
    )

if __name__ == '__main__':
    main()
