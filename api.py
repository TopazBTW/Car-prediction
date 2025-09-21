# API for Vehicle Price Prediction

from flask import Flask, request, jsonify
import pandas as pd
import pickle
import numpy as np
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Load the saved model
def load_model(filename='models/vehicle_price_model.pkl'):
    try:
        with open(filename, 'rb') as file:
            model = pickle.load(file)
        print(f"Model loaded from {filename}")
        return model
    except Exception as e:
        print(f"Error loading model: {e}")
        return None

model = load_model()

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get data from request
        data = request.json

        # Convert to DataFrame
        input_data = pd.DataFrame([data])

        # Make prediction
        prediction = model.predict(input_data)

        # Return prediction
        return jsonify({
            'success': True,
            'predicted_price': float(prediction[0]),
            'formatted_price': f"${prediction[0]:,.2f}"
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy', 'model_loaded': model is not None})

if __name__ == '__main__':
    app.run(debug=True, port=5000)