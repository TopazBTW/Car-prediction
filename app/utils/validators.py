"""
Validation utilities for the Car Price Predictor application.
"""
from typing import Dict, Any, List, Tuple
import pandas as pd

def validate_vehicle_data(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    """
    Validate vehicle data for prediction.
    
    Args:
        data: Dictionary containing vehicle features
        
    Returns:
        Tuple of (is_valid, error_messages)
    """
    errors = []
    
    # Required fields
    required_fields = [
        'Brand', 'Model', 'Year', 'KM_Driven', 
        'Fuel', 'Seller_Type', 'Transmission', 'Owner'
    ]
    
    for field in required_fields:
        if field not in data:
            errors.append(f"Missing required field: {field}")
    
    if errors:
        return False, errors
    
    # Validate data types and ranges
    try:
        year = int(data['Year'])
        if year < 1900 or year > 2030:
            errors.append("Year must be between 1900 and 2030")
    except (ValueError, TypeError):
        errors.append("Year must be a valid integer")
    
    try:
        km_driven = int(data['KM_Driven'])
        if km_driven < 0:
            errors.append("KM_Driven must be non-negative")
    except (ValueError, TypeError):
        errors.append("KM_Driven must be a valid integer")
    
    # Validate categorical fields
    valid_brands = ['Toyota', 'Honda', 'Ford', 'BMW', 'Mercedes', 'Audi', 'Volkswagen', 'Hyundai']
    if data['Brand'] not in valid_brands:
        errors.append(f"Invalid brand. Must be one of: {valid_brands}")
    
    valid_models = ['Sedan', 'SUV', 'Hatchback', 'Coupe', 'Truck', 'Convertible']
    if data['Model'] not in valid_models:
        errors.append(f"Invalid model. Must be one of: {valid_models}")
    
    valid_fuels = ['Petrol', 'Diesel', 'Electric', 'Hybrid']
    if data['Fuel'] not in valid_fuels:
        errors.append(f"Invalid fuel type. Must be one of: {valid_fuels}")
    
    valid_sellers = ['Individual', 'Dealer', 'Trustmark Dealer']
    if data['Seller_Type'] not in valid_sellers:
        errors.append(f"Invalid seller type. Must be one of: {valid_sellers}")
    
    valid_transmissions = ['Manual', 'Automatic']
    if data['Transmission'] not in valid_transmissions:
        errors.append(f"Invalid transmission. Must be one of: {valid_transmissions}")
    
    valid_owners = ['First Owner', 'Second Owner', 'Third Owner', 'Fourth & Above Owner']
    if data['Owner'] not in valid_owners:
        errors.append(f"Invalid owner type. Must be one of: {valid_owners}")
    
    return len(errors) == 0, errors

def sanitize_input(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Sanitize input data to prevent injection attacks.
    
    Args:
        data: Raw input data
        
    Returns:
        Sanitized data dictionary
    """
    sanitized = {}
    
    for key, value in data.items():
        if isinstance(value, str):
            # Remove potentially dangerous characters
            sanitized[key] = value.strip()
        elif isinstance(value, (int, float)):
            sanitized[key] = value
        else:
            sanitized[key] = str(value).strip()
    
    return sanitized
