"""
API routes for the Car Price Predictor application.
"""
import logging
from flask import Blueprint, request, jsonify, current_app
from marshmallow import Schema, fields, ValidationError
from app.models.model_manager import ModelManager
from app.utils.validators import validate_vehicle_data
from app.utils.logger import get_logger

logger = get_logger(__name__)

# Create blueprint
api_bp = Blueprint('api', __name__, url_prefix='/api/v1')

# Initialize model manager
model_manager = None

def init_model_manager():
    """Initialize the model manager."""
    global model_manager
    try:
        model_path = current_app.config.get('MODEL_PATH')
        model_manager = ModelManager(str(model_path))
        logger.info("Model manager initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize model manager: {e}")
        raise

# Request/Response Schemas
class VehicleDataSchema(Schema):
    """Schema for vehicle data validation."""
    Brand = fields.Str(required=True, validate=lambda x: x in [
        'Toyota', 'Honda', 'Ford', 'BMW', 'Mercedes', 'Audi', 'Volkswagen', 'Hyundai'
    ])
    Model = fields.Str(required=True, validate=lambda x: x in [
        'Sedan', 'SUV', 'Hatchback', 'Coupe', 'Truck', 'Convertible'
    ])
    Year = fields.Int(required=True, validate=lambda x: 1900 <= x <= 2030)
    KM_Driven = fields.Int(required=True, validate=lambda x: x >= 0)
    Fuel = fields.Str(required=True, validate=lambda x: x in [
        'Petrol', 'Diesel', 'Electric', 'Hybrid'
    ])
    Seller_Type = fields.Str(required=True, validate=lambda x: x in [
        'Individual', 'Dealer', 'Trustmark Dealer'
    ])
    Transmission = fields.Str(required=True, validate=lambda x: x in [
        'Manual', 'Automatic'
    ])
    Owner = fields.Str(required=True, validate=lambda x: x in [
        'First Owner', 'Second Owner', 'Third Owner', 'Fourth & Above Owner'
    ])

class PredictionResponseSchema(Schema):
    """Schema for prediction response."""
    success = fields.Bool(required=True)
    predicted_price = fields.Float(allow_none=True)
    formatted_price = fields.Str(allow_none=True)
    confidence = fields.Float(allow_none=True)
    model_info = fields.Dict(allow_none=True)
    error = fields.Str(allow_none=True)
    error_type = fields.Str(allow_none=True)

# API Routes
@api_bp.route('/predict', methods=['POST'])
def predict_price():
    """
    Predict vehicle price based on input features.
    
    Returns:
        JSON response with prediction results
    """
    try:
        # Validate request
        if not request.is_json:
            return jsonify({
                'success': False,
                'error': 'Request must be JSON',
                'error_type': 'ContentTypeError'
            }), 400
        
        # Parse and validate input data
        schema = VehicleDataSchema()
        try:
            vehicle_data = schema.load(request.json)
        except ValidationError as e:
            return jsonify({
                'success': False,
                'error': f'Validation error: {e.messages}',
                'error_type': 'ValidationError'
            }), 400
        
        # Make prediction
        result = model_manager.predict(vehicle_data)
        
        if result['success']:
            logger.info(f"Successful prediction for {vehicle_data['Brand']} {vehicle_data['Model']}")
            return jsonify(result), 200
        else:
            logger.error(f"Prediction failed: {result.get('error')}")
            return jsonify(result), 500
            
    except Exception as e:
        logger.error(f"Unexpected error in predict_price: {e}")
        return jsonify({
            'success': False,
            'error': 'Internal server error',
            'error_type': 'InternalError'
        }), 500

@api_bp.route('/health', methods=['GET'])
def health_check():
    """
    Health check endpoint for monitoring.
    
    Returns:
        JSON response with system status
    """
    try:
        model_info = model_manager.get_model_info() if model_manager else None
        
        status = {
            'status': 'healthy',
            'model_loaded': model_info['is_loaded'] if model_info else False,
            'version': current_app.config.get('API_VERSION', '1.0.0'),
            'model_info': model_info
        }
        
        return jsonify(status), 200
        
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return jsonify({
            'status': 'unhealthy',
            'error': str(e)
        }), 500

@api_bp.route('/model/info', methods=['GET'])
def get_model_info():
    """
    Get detailed information about the loaded model.
    
    Returns:
        JSON response with model information
    """
    try:
        if not model_manager:
            return jsonify({
                'success': False,
                'error': 'Model manager not initialized'
            }), 500
        
        model_info = model_manager.get_model_info()
        return jsonify({
            'success': True,
            'model_info': model_info
        }), 200
        
    except Exception as e:
        logger.error(f"Error getting model info: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@api_bp.route('/features', methods=['GET'])
def get_feature_info():
    """
    Get information about supported features and their valid values.
    
    Returns:
        JSON response with feature information
    """
    feature_info = {
        'Brand': {
            'type': 'categorical',
            'required': True,
            'valid_values': ['Toyota', 'Honda', 'Ford', 'BMW', 'Mercedes', 'Audi', 'Volkswagen', 'Hyundai']
        },
        'Model': {
            'type': 'categorical',
            'required': True,
            'valid_values': ['Sedan', 'SUV', 'Hatchback', 'Coupe', 'Truck', 'Convertible']
        },
        'Year': {
            'type': 'numerical',
            'required': True,
            'min_value': 1900,
            'max_value': 2030
        },
        'KM_Driven': {
            'type': 'numerical',
            'required': True,
            'min_value': 0
        },
        'Fuel': {
            'type': 'categorical',
            'required': True,
            'valid_values': ['Petrol', 'Diesel', 'Electric', 'Hybrid']
        },
        'Seller_Type': {
            'type': 'categorical',
            'required': True,
            'valid_values': ['Individual', 'Dealer', 'Trustmark Dealer']
        },
        'Transmission': {
            'type': 'categorical',
            'required': True,
            'valid_values': ['Manual', 'Automatic']
        },
        'Owner': {
            'type': 'categorical',
            'required': True,
            'valid_values': ['First Owner', 'Second Owner', 'Third Owner', 'Fourth & Above Owner']
        }
    }
    
    return jsonify({
        'success': True,
        'features': feature_info
    }), 200

@api_bp.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({
        'success': False,
        'error': 'Endpoint not found',
        'error_type': 'NotFoundError'
    }), 404

@api_bp.errorhandler(405)
def method_not_allowed(error):
    """Handle 405 errors."""
    return jsonify({
        'success': False,
        'error': 'Method not allowed',
        'error_type': 'MethodNotAllowedError'
    }), 405

@api_bp.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    logger.error(f"Internal server error: {error}")
    return jsonify({
        'success': False,
        'error': 'Internal server error',
        'error_type': 'InternalError'
    }), 500
