"""
Pytest configuration and fixtures for the Car Price Predictor tests.
"""
import pytest
import tempfile
import os
from pathlib import Path

@pytest.fixture(scope="session")
def test_data_dir():
    """Create a temporary directory for test data."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)

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

@pytest.fixture
def invalid_vehicle_data():
    """Invalid vehicle data for testing validation."""
    return {
        "Brand": "InvalidBrand",
        "Model": "Sedan",
        "Year": 1800,  # Invalid year
        "KM_Driven": -1000,  # Invalid mileage
        "Fuel": "InvalidFuel",
        "Seller_Type": "Individual",
        "Transmission": "Manual",
        "Owner": "First Owner"
    }
