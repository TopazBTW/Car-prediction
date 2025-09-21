# Car Price Predictor API Documentation

## Overview

The Car Price Predictor API is a RESTful web service that provides machine learning-powered vehicle price predictions. Built with Flask and scikit-learn, it offers accurate price estimates based on vehicle characteristics.

## Base URL

```
http://localhost:5000/api/v1
```

## Authentication

Currently, the API does not require authentication. In production, consider implementing API keys or OAuth2.

## Endpoints

### 1. Health Check

**GET** `/health`

Check the health status of the API and model.

#### Response

```json
{
  "status": "healthy",
  "model_loaded": true,
  "version": "1.0.0",
  "model_info": {
    "model_type": "Pipeline",
    "loaded_at": "2024-01-15T10:30:00",
    "model_path": "/app/models/vehicle_price_model.pkl"
  }
}
```

#### Status Codes

- `200 OK` - Service is healthy
- `500 Internal Server Error` - Service is unhealthy

---

### 2. Price Prediction

**POST** `/predict`

Predict the market price of a vehicle based on its characteristics.

#### Request Body

```json
{
  "Brand": "Toyota",
  "Model": "Sedan",
  "Year": 2018,
  "KM_Driven": 50000,
  "Fuel": "Petrol",
  "Seller_Type": "Individual",
  "Transmission": "Manual",
  "Owner": "First Owner"
}
```

#### Field Descriptions

| Field | Type | Required | Description | Valid Values |
|-------|------|----------|-------------|--------------|
| `Brand` | string | Yes | Vehicle manufacturer | Toyota, Honda, Ford, BMW, Mercedes, Audi, Volkswagen, Hyundai |
| `Model` | string | Yes | Vehicle type/model | Sedan, SUV, Hatchback, Coupe, Truck, Convertible |
| `Year` | integer | Yes | Manufacturing year | 1900-2030 |
| `KM_Driven` | integer | Yes | Total kilometers driven | ≥ 0 |
| `Fuel` | string | Yes | Fuel type | Petrol, Diesel, Electric, Hybrid |
| `Seller_Type` | string | Yes | Type of seller | Individual, Dealer, Trustmark Dealer |
| `Transmission` | string | Yes | Transmission type | Manual, Automatic |
| `Owner` | string | Yes | Ownership history | First Owner, Second Owner, Third Owner, Fourth & Above Owner |

#### Response

**Success Response (200 OK)**

```json
{
  "success": true,
  "predicted_price": 447159.98,
  "formatted_price": "$447,159.98",
  "confidence": 0.85,
  "model_info": {
    "model_type": "Pipeline",
    "loaded_at": "2024-01-15T10:30:00"
  },
  "input_features": {
    "Brand": "Toyota",
    "Model": "Sedan",
    "Year": 2018,
    "KM_Driven": 50000,
    "Fuel": "Petrol",
    "Seller_Type": "Individual",
    "Transmission": "Manual",
    "Owner": "First Owner"
  }
}
```

**Error Response (400 Bad Request)**

```json
{
  "success": false,
  "error": "Validation error: {'Year': ['Must be between 1900 and 2030']}",
  "error_type": "ValidationError"
}
```

#### Status Codes

- `200 OK` - Prediction successful
- `400 Bad Request` - Invalid input data
- `500 Internal Server Error` - Server error

---

### 3. Model Information

**GET** `/model/info`

Get detailed information about the loaded machine learning model.

#### Response

```json
{
  "success": true,
  "model_info": {
    "model_metadata": {
      "model_type": "Pipeline",
      "loaded_at": "2024-01-15T10:30:00",
      "model_path": "/app/models/vehicle_price_model.pkl"
    },
    "feature_names": ["Brand", "Model", "Year", "KM_Driven", "Fuel", "Seller_Type", "Transmission", "Owner"],
    "model_type": "Pipeline",
    "is_loaded": true
  }
}
```

---

### 4. Feature Information

**GET** `/features`

Get information about supported features and their valid values.

#### Response

```json
{
  "success": true,
  "features": {
    "Brand": {
      "type": "categorical",
      "required": true,
      "valid_values": ["Toyota", "Honda", "Ford", "BMW", "Mercedes", "Audi", "Volkswagen", "Hyundai"]
    },
    "Model": {
      "type": "categorical",
      "required": true,
      "valid_values": ["Sedan", "SUV", "Hatchback", "Coupe", "Truck", "Convertible"]
    },
    "Year": {
      "type": "numerical",
      "required": true,
      "min_value": 1900,
      "max_value": 2030
    },
    "KM_Driven": {
      "type": "numerical",
      "required": true,
      "min_value": 0
    },
    "Fuel": {
      "type": "categorical",
      "required": true,
      "valid_values": ["Petrol", "Diesel", "Electric", "Hybrid"]
    },
    "Seller_Type": {
      "type": "categorical",
      "required": true,
      "valid_values": ["Individual", "Dealer", "Trustmark Dealer"]
    },
    "Transmission": {
      "type": "categorical",
      "required": true,
      "valid_values": ["Manual", "Automatic"]
    },
    "Owner": {
      "type": "categorical",
      "required": true,
      "valid_values": ["First Owner", "Second Owner", "Third Owner", "Fourth & Above Owner"]
    }
  }
}
```

## Error Handling

The API uses standard HTTP status codes and returns error information in JSON format.

### Error Response Format

```json
{
  "success": false,
  "error": "Error description",
  "error_type": "ErrorType"
}
```

### Common Error Types

- `ValidationError` - Input validation failed
- `ContentTypeError` - Wrong content type
- `NotFoundError` - Endpoint not found
- `MethodNotAllowedError` - HTTP method not allowed
- `InternalError` - Internal server error

## Rate Limiting

Currently, there are no rate limits implemented. In production, consider implementing rate limiting to prevent abuse.

## CORS

The API supports Cross-Origin Resource Sharing (CORS) for web applications. Allowed origins are configurable.

## Examples

### cURL Examples

#### Health Check

```bash
curl -X GET http://localhost:5000/api/v1/health
```

#### Price Prediction

```bash
curl -X POST http://localhost:5000/api/v1/predict \
  -H "Content-Type: application/json" \
  -d '{
    "Brand": "Toyota",
    "Model": "Sedan",
    "Year": 2018,
    "KM_Driven": 50000,
    "Fuel": "Petrol",
    "Seller_Type": "Individual",
    "Transmission": "Manual",
    "Owner": "First Owner"
  }'
```

### Python Examples

```python
import requests

# Health check
response = requests.get('http://localhost:5000/api/v1/health')
print(response.json())

# Price prediction
vehicle_data = {
    "Brand": "Toyota",
    "Model": "Sedan",
    "Year": 2018,
    "KM_Driven": 50000,
    "Fuel": "Petrol",
    "Seller_Type": "Individual",
    "Transmission": "Manual",
    "Owner": "First Owner"
}

response = requests.post(
    'http://localhost:5000/api/v1/predict',
    json=vehicle_data
)

if response.status_code == 200:
    result = response.json()
    print(f"Predicted price: {result['formatted_price']}")
    print(f"Confidence: {result['confidence']:.2f}")
else:
    print(f"Error: {response.json()['error']}")
```

### JavaScript Examples

```javascript
// Health check
fetch('http://localhost:5000/api/v1/health')
  .then(response => response.json())
  .then(data => console.log(data));

// Price prediction
const vehicleData = {
  Brand: "Toyota",
  Model: "Sedan",
  Year: 2018,
  KM_Driven: 50000,
  Fuel: "Petrol",
  Seller_Type: "Individual",
  Transmission: "Manual",
  Owner: "First Owner"
};

fetch('http://localhost:5000/api/v1/predict', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify(vehicleData)
})
.then(response => response.json())
.then(data => {
  if (data.success) {
    console.log(`Predicted price: ${data.formatted_price}`);
    console.log(`Confidence: ${data.confidence.toFixed(2)}`);
  } else {
    console.error(`Error: ${data.error}`);
  }
});
```

## Model Performance

The current model achieves the following performance metrics:

- **R² Score**: 0.6893 (68.93% variance explained)
- **RMSE**: 307,902.14 (Root Mean Square Error)
- **MAE**: Mean Absolute Error
- **Training Data**: 4,340 vehicle records

## Changelog

### Version 1.0.0
- Initial release
- Basic price prediction functionality
- Health check endpoint
- Model information endpoint
- Feature information endpoint

## Support

For questions or issues, please contact the development team or create an issue in the project repository.
