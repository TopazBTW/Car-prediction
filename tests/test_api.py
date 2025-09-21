"""
Test suite for the Car Price Predictor API.
"""
import pytest
import json
from app import create_app
from app.models.model_manager import ModelManager

@pytest.fixture
def app():
    """Create test application."""
    app = create_app('testing')
    return app

@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()

@pytest.fixture
def sample_vehicle_data():
    """Sample vehicle data for testing."""
    return {
        "Brand": "Toyota",
        "Model": "Sedan",
        "Year": 2018,
        "KM_Driven": 50000,
        "Fuel": "Petrol",
        "Seller_Type": "Individual",
        "Transmission": "Manual",
        "Owner": "First Owner"
    }

class TestHealthEndpoint:
    """Test health check endpoint."""
    
    def test_health_check_success(self, client):
        """Test successful health check."""
        response = client.get('/api/v1/health')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert data['status'] == 'healthy'
        assert 'model_loaded' in data
        assert 'version' in data

class TestPredictionEndpoint:
    """Test prediction endpoint."""
    
    def test_predict_success(self, client, sample_vehicle_data):
        """Test successful price prediction."""
        response = client.post(
            '/api/v1/predict',
            data=json.dumps(sample_vehicle_data),
            content_type='application/json'
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        
        assert data['success'] is True
        assert 'predicted_price' in data
        assert 'formatted_price' in data
        assert 'confidence' in data
        assert isinstance(data['predicted_price'], (int, float))
        assert data['predicted_price'] > 0
    
    def test_predict_missing_fields(self, client):
        """Test prediction with missing required fields."""
        incomplete_data = {
            "Brand": "Toyota",
            "Year": 2018
            # Missing other required fields
        }
        
        response = client.post(
            '/api/v1/predict',
            data=json.dumps(incomplete_data),
            content_type='application/json'
        )
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['success'] is False
        assert 'error' in data
    
    def test_predict_invalid_data(self, client):
        """Test prediction with invalid data."""
        invalid_data = {
            "Brand": "InvalidBrand",
            "Model": "Sedan",
            "Year": 1800,  # Invalid year
            "KM_Driven": -1000,  # Invalid mileage
            "Fuel": "InvalidFuel",
            "Seller_Type": "Individual",
            "Transmission": "Manual",
            "Owner": "First Owner"
        }
        
        response = client.post(
            '/api/v1/predict',
            data=json.dumps(invalid_data),
            content_type='application/json'
        )
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['success'] is False
        assert 'error' in data
    
    def test_predict_wrong_content_type(self, client, sample_vehicle_data):
        """Test prediction with wrong content type."""
        response = client.post(
            '/api/v1/predict',
            data=json.dumps(sample_vehicle_data),
            content_type='text/plain'
        )
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['success'] is False
        assert 'error' in data

class TestModelInfoEndpoint:
    """Test model information endpoint."""
    
    def test_model_info_success(self, client):
        """Test successful model info retrieval."""
        response = client.get('/api/v1/model/info')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert data['success'] is True
        assert 'model_info' in data

class TestFeaturesEndpoint:
    """Test features information endpoint."""
    
    def test_features_info_success(self, client):
        """Test successful features info retrieval."""
        response = client.get('/api/v1/features')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert data['success'] is True
        assert 'features' in data
        
        # Check that all required features are present
        required_features = [
            'Brand', 'Model', 'Year', 'KM_Driven',
            'Fuel', 'Seller_Type', 'Transmission', 'Owner'
        ]
        
        for feature in required_features:
            assert feature in data['features']

class TestErrorHandling:
    """Test error handling."""
    
    def test_404_error(self, client):
        """Test 404 error handling."""
        response = client.get('/api/v1/nonexistent')
        assert response.status_code == 404
        
        data = json.loads(response.data)
        assert data['success'] is False
        assert 'error' in data
    
    def test_method_not_allowed(self, client):
        """Test 405 error handling."""
        response = client.get('/api/v1/predict')
        assert response.status_code == 405
        
        data = json.loads(response.data)
        assert data['success'] is False
        assert 'error' in data

class TestModelManager:
    """Test ModelManager class."""
    
    def test_model_manager_initialization(self):
        """Test model manager initialization."""
        # This test assumes the model file exists
        try:
            manager = ModelManager('models/vehicle_price_model.pkl')
            assert manager.model is not None
            assert manager.model_metadata is not None
        except FileNotFoundError:
            pytest.skip("Model file not found")
    
    def test_model_prediction(self, sample_vehicle_data):
        """Test model prediction."""
        try:
            manager = ModelManager('models/vehicle_price_model.pkl')
            result = manager.predict(sample_vehicle_data)
            
            assert result['success'] is True
            assert 'predicted_price' in result
            assert 'confidence' in result
            assert result['predicted_price'] > 0
        except FileNotFoundError:
            pytest.skip("Model file not found")
    
    def test_model_validation(self, sample_vehicle_data):
        """Test model input validation."""
        try:
            manager = ModelManager('models/vehicle_price_model.pkl')
            
            # Test with invalid data
            invalid_data = sample_vehicle_data.copy()
            invalid_data['Year'] = 1800  # Invalid year
            
            result = manager.predict(invalid_data)
            assert result['success'] is False
            assert 'error' in result
        except FileNotFoundError:
            pytest.skip("Model file not found")
