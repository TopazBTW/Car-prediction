import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_squared_error, r2_score
import pickle
import os

# Load the dataset
def load_data():
    """Load the vehicle dataset from your file"""
    df = pd.read_csv('CarPrice.csv')
    print(f"Data loaded successfully with {df.shape[0]} rows and {df.shape[1]} columns")
    return df

def preprocess_data(df):
    """Perform data preprocessing"""
    # Make a copy to avoid modifying the original
    data = df.copy()

    # Check for missing values
    print("Missing values in each column:")
    print(data.isnull().sum())

    # Fill missing values if any
    # Note: Modify this based on your specific dataset
    if data.isnull().sum().sum() > 0:
        # Fill numerical columns with median
        numerical_cols = data.select_dtypes(include=['int64', 'float64']).columns
        for col in numerical_cols:
            if data[col].isnull().sum() > 0:
                data[col] = data[col].fillna(data[col].median())

        # Fill categorical columns with mode
        categorical_cols = data.select_dtypes(include=['object']).columns
        for col in categorical_cols:
            if data[col].isnull().sum() > 0:
                data[col] = data[col].fillna(data[col].mode()[0])

    # Ensure price column is named 'Selling_Price' (adjust if needed)
    if 'Selling_Price' not in data.columns:
        print("Warning: 'Selling_Price' column not found. Using alternate price column if available.")
        price_cols = [col for col in data.columns if 'price' in col.lower() or 'cost' in col.lower()]
        if price_cols:
            data = data.rename(columns={price_cols[0]: 'Selling_Price'})
        else:
            raise ValueError("No price column found in the dataset.")

    return data

def build_model(df):
    """Build and train the price prediction model"""
    # Separate features and target
    X = df.drop('Selling_Price', axis=1)
    y = df['Selling_Price']

    # Identify categorical and numerical columns
    categorical_cols = X.select_dtypes(include=['object']).columns.tolist()
    numerical_cols = X.select_dtypes(include=['int64', 'float64']).columns.tolist()

    print(f"Categorical features: {categorical_cols}")
    print(f"Numerical features: {numerical_cols}")

    # Create preprocessor
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', 'passthrough', numerical_cols),
            ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_cols)
        ])

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Create and train the model
    model = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('regressor', RandomForestRegressor(n_estimators=100, random_state=42))
    ])

    model.fit(X_train, y_train)

    # Evaluate model
    y_pred = model.predict(X_test)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    r2 = r2_score(y_test, y_pred)

    print(f"Model Performance:")
    print(f"Root Mean Squared Error (RMSE): {rmse:.2f}")
    print(f"R² Score: {r2:.4f}")

    return model, rmse, r2

def save_model(model, filename='models/vehicle_price_model.pkl'):
    """Save the trained model"""
    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    # Save the model
    with open(filename, 'wb') as file:
        pickle.dump(model, file)
    print(f"Model saved to {filename}")

def load_model(filename='models/vehicle_price_model.pkl'):
    """Load a saved model"""
    with open(filename, 'rb') as file:
        model = pickle.load(file)
    print(f"Model loaded from {filename}")
    return model

def predict_price(model, input_data):
    """Make a price prediction for new vehicle data"""
    # Input data should be a pandas DataFrame with the same columns as training data
    # (except the target column)
    prediction = model.predict(input_data)
    return prediction[0]

def main():
    # Load and preprocess data
    df = load_data()
    df_processed = preprocess_data(df)

    # Build and train model
    model, rmse, r2 = build_model(df_processed)

    # Save the model
    save_model(model)

    print("Model training completed!")

if __name__ == "__main__":
    main()