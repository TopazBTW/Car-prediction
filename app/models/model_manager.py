"""
Model management module for the Car Price Predictor.
Handles model loading, prediction, and validation.
"""
import pickle
import logging
import numpy as np
import pandas as pd
from pathlib import Path
from typing import Dict, Any, Optional, Tuple
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error

logger = logging.getLogger(__name__)

class ModelManager:
    """Manages the machine learning model for price prediction."""
    
    def __init__(self, model_path: str):
        """
        Initialize the ModelManager.
        
        Args:
            model_path: Path to the saved model file
        """
        self.model_path = Path(model_path)
        self.model = None
        self.feature_names = None
        self.model_metadata = {}
        self._load_model()
    
    def _load_model(self) -> None:
        """Load the model from the specified path."""
        try:
            if not self.model_path.exists():
                raise FileNotFoundError(f"Model file not found: {self.model_path}")
            
            with open(self.model_path, 'rb') as file:
                self.model = pickle.load(file)
            
            logger.info(f"Model loaded successfully from {self.model_path}")
            
            # Extract feature names if available
            if hasattr(self.model, 'feature_names_in_'):
                self.feature_names = self.model.feature_names_in_.tolist()
            
            # Store model metadata
            self.model_metadata = {
                'model_type': type(self.model).__name__,
                'loaded_at': pd.Timestamp.now().isoformat(),
                'model_path': str(self.model_path)
            }
            
        except Exception as e:
            logger.error(f"Error loading model: {e}")
            raise
    
    def predict(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Make a price prediction for the given input data.
        
        Args:
            input_data: Dictionary containing vehicle features
            
        Returns:
            Dictionary containing prediction results and metadata
        """
        try:
            # Validate input data
            self._validate_input(input_data)
            
            # Convert to DataFrame
            df = pd.DataFrame([input_data])
            
            # Make prediction
            prediction = self.model.predict(df)[0]
            
            # Calculate confidence (simplified - in production, use proper uncertainty quantification)
            confidence = self._calculate_confidence(prediction, input_data)
            
            # Format results
            result = {
                'success': True,
                'predicted_price': float(prediction),
                'formatted_price': f"${prediction:,.2f}",
                'confidence': confidence,
                'model_info': self.model_metadata,
                'input_features': input_data
            }
            
            logger.info(f"Prediction made: ${prediction:,.2f} (confidence: {confidence:.2f})")
            return result
            
        except Exception as e:
            logger.error(f"Error making prediction: {e}")
            return {
                'success': False,
                'error': str(e),
                'error_type': type(e).__name__
            }
    
    def _validate_input(self, input_data: Dict[str, Any]) -> None:
        """
        Validate input data for prediction.
        
        Args:
            input_data: Dictionary containing vehicle features
            
        Raises:
            ValueError: If input data is invalid
        """
        required_fields = [
            'Brand', 'Model', 'Year', 'KM_Driven', 
            'Fuel', 'Seller_Type', 'Transmission', 'Owner'
        ]
        
        # Check required fields
        missing_fields = [field for field in required_fields if field not in input_data]
        if missing_fields:
            raise ValueError(f"Missing required fields: {missing_fields}")
        
        # Validate data types and ranges
        if not isinstance(input_data['Year'], (int, float)) or input_data['Year'] < 1900 or input_data['Year'] > 2030:
            raise ValueError("Year must be a number between 1900 and 2030")
        
        if not isinstance(input_data['KM_Driven'], (int, float)) or input_data['KM_Driven'] < 0:
            raise ValueError("KM_Driven must be a non-negative number")
        
        # Validate categorical fields
        valid_brands = ['Toyota', 'Honda', 'Ford', 'BMW', 'Mercedes', 'Audi', 'Volkswagen', 'Hyundai']
        if input_data['Brand'] not in valid_brands:
            raise ValueError(f"Invalid brand. Must be one of: {valid_brands}")
        
        valid_fuels = ['Petrol', 'Diesel', 'Electric', 'Hybrid']
        if input_data['Fuel'] not in valid_fuels:
            raise ValueError(f"Invalid fuel type. Must be one of: {valid_fuels}")
    
    def _calculate_confidence(self, prediction: float, input_data: Dict[str, Any]) -> float:
        """
        Calculate prediction confidence (simplified implementation).
        
        Args:
            prediction: Predicted price
            input_data: Input features
            
        Returns:
            Confidence score between 0 and 1
        """
        # Simple confidence calculation based on feature completeness and ranges
        confidence = 0.8  # Base confidence
        
        # Adjust based on year (newer cars have more predictable prices)
        year = input_data.get('Year', 2020)
        if 2015 <= year <= 2023:
            confidence += 0.1
        elif year < 2010:
            confidence -= 0.1
        
        # Adjust based on mileage
        km_driven = input_data.get('KM_Driven', 50000)
        if km_driven < 100000:
            confidence += 0.05
        elif km_driven > 200000:
            confidence -= 0.05
        
        return max(0.1, min(1.0, confidence))
    
    def get_model_info(self) -> Dict[str, Any]:
        """
        Get information about the loaded model.
        
        Returns:
            Dictionary containing model information
        """
        return {
            'model_metadata': self.model_metadata,
            'feature_names': self.feature_names,
            'model_type': type(self.model).__name__ if self.model else None,
            'is_loaded': self.model is not None
        }
    
    def evaluate_model(self, X_test: pd.DataFrame, y_test: pd.Series) -> Dict[str, float]:
        """
        Evaluate model performance on test data.
        
        Args:
            X_test: Test features
            y_test: Test targets
            
        Returns:
            Dictionary containing evaluation metrics
        """
        if self.model is None:
            raise ValueError("Model not loaded")
        
        y_pred = self.model.predict(X_test)
        
        metrics = {
            'r2_score': r2_score(y_test, y_pred),
            'rmse': np.sqrt(mean_squared_error(y_test, y_pred)),
            'mae': mean_absolute_error(y_test, y_pred),
            'mape': np.mean(np.abs((y_test - y_pred) / y_test)) * 100
        }
        
        return metrics
