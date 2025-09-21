# 🚗 Smart Car Price Predictor

A sophisticated machine learning web application that predicts vehicle market prices using advanced AI algorithms. Built with Flask, scikit-learn, and modern web technologies.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-2.0+-green.svg)
![scikit-learn](https://img.shields.io/badge/scikit--learn-1.0+-orange.svg)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-purple.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 🌟 Features

### 🤖 **Advanced AI/ML**
- **Random Forest Regression** with hyperparameter optimization
- **Feature Engineering** with categorical encoding
- **Model Validation** with cross-validation and metrics
- **Real-time Predictions** with sub-second response times
- **Model Persistence** with pickle serialization

### 🎨 **Modern Web Interface**
- **Responsive Design** optimized for all devices
- **Interactive Animations** with CSS3 and JavaScript
- **Real-time Validation** with instant feedback
- **Professional UI/UX** with modern design patterns
- **Accessibility Compliant** with ARIA labels

### 🚀 **Production-Ready Features**
- **RESTful API** with comprehensive error handling
- **CORS Support** for cross-origin requests
- **Input Validation** and sanitization
- **Logging System** with structured logging
- **Health Monitoring** with status endpoints
- **Docker Support** for containerized deployment

### 📊 **Data Science Capabilities**
- **Dataset Analysis** with 4,340+ vehicle records
- **Feature Importance** analysis and visualization
- **Model Performance** tracking with R² score of 0.6893
- **Data Preprocessing** pipeline with missing value handling
- **Cross-validation** for robust model evaluation

## 🛠️ Technology Stack

### **Backend**
- **Python 3.8+** - Core programming language
- **Flask** - Web framework and API development
- **scikit-learn** - Machine learning library
- **pandas** - Data manipulation and analysis
- **numpy** - Numerical computing
- **pickle** - Model serialization

### **Frontend**
- **HTML5** - Semantic markup
- **CSS3** - Modern styling with animations
- **JavaScript (ES6+)** - Interactive functionality
- **Bootstrap 5** - Responsive UI framework
- **Font Awesome** - Icon library

### **DevOps & Deployment**
- **Docker** - Containerization
- **Git** - Version control
- **pytest** - Testing framework
- **logging** - Structured logging

## 📁 Project Structure

```
CAR predict/
├── 📁 app/                    # Main application package
│   ├── 📁 models/            # ML models and preprocessing
│   ├── 📁 api/               # API routes and endpoints
│   ├── 📁 utils/              # Utility functions
│   └── 📁 static/             # Static files (CSS, JS, images)
├── 📁 tests/                  # Test suite
├── 📁 docs/                   # Documentation
├── 📁 data/                   # Dataset and processed data
├── 📁 config/                 # Configuration files
├── 🐳 Dockerfile             # Docker configuration
├── 📄 requirements.txt        # Python dependencies
├── 📄 README.md              # Project documentation
└── 📄 .gitignore             # Git ignore rules
```

## 🚀 Quick Start

### **Prerequisites**
- Python 3.8 or higher
- pip (Python package installer)
- Git

### **Installation**

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/car-price-predictor.git
   cd car-price-predictor
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Train the model**
   ```bash
   python train_model.py
   ```

5. **Start the application**
   ```bash
   python api.py
   ```

6. **Open your browser**
   Navigate to `http://localhost:5000` to access the web interface.

## 🐳 Docker Deployment

### **Build and run with Docker**

```bash
# Build the Docker image
docker build -t car-price-predictor .

# Run the container
docker run -p 5000:5000 car-price-predictor
```

## 🧪 Testing

### **Run the test suite**

```bash
# Run all tests
pytest tests/

# Run with coverage
pytest --cov=app tests/

# Run specific test file
pytest tests/test_api.py
```

### **Test Coverage**
- **API Endpoints** - Comprehensive endpoint testing
- **Model Validation** - ML model accuracy testing
- **Input Validation** - Data validation testing
- **Error Handling** - Exception handling testing

## 📊 Model Performance

### **Metrics**
- **R² Score**: 0.6893 (68.93% variance explained)
- **RMSE**: 307,902.14 (Root Mean Square Error)
- **Training Data**: 4,340 vehicle records
- **Features**: 8 input features (Brand, Model, Year, etc.)

### **Feature Importance**
1. **Year** - Most significant factor in price prediction
2. **KM_Driven** - Mileage impact on vehicle value
3. **Brand** - Manufacturer reputation and market position
4. **Fuel Type** - Fuel efficiency and environmental factors
5. **Model Type** - Vehicle category and market demand

## 🔧 API Documentation

### **Endpoints**

#### **POST /predict**
Predict vehicle price based on input features.

**Request Body:**
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

**Response:**
```json
{
  "success": true,
  "predicted_price": 447159.98,
  "formatted_price": "$447,159.98",
  "confidence": 0.85
}
```

#### **GET /health**
Health check endpoint for monitoring.

**Response:**
```json
{
  "status": "healthy",
  "model_loaded": true,
  "version": "1.0.0"
}
```

## 🎯 Use Cases

### **For Buyers**
- **Market Research** - Understand fair market value
- **Negotiation** - Use data-driven pricing for negotiations
- **Budget Planning** - Plan vehicle purchase budgets

### **For Sellers**
- **Pricing Strategy** - Set competitive market prices
- **Market Analysis** - Understand pricing trends
- **Inventory Management** - Optimize vehicle pricing

### **For Dealers**
- **Inventory Valuation** - Assess vehicle portfolio value
- **Market Intelligence** - Track pricing trends
- **Customer Service** - Provide instant price estimates

## 🔮 Future Enhancements

### **Planned Features**
- **Multiple Model Support** - Linear Regression, XGBoost, Neural Networks
- **Real-time Data Integration** - Live market data feeds
- **Advanced Analytics** - Price trend analysis and forecasting
- **User Authentication** - User accounts and prediction history
- **API Rate Limiting** - Production-ready API management
- **Model Versioning** - A/B testing and model comparison

### **Technical Improvements**
- **Microservices Architecture** - Scalable service design
- **Database Integration** - PostgreSQL/MongoDB for data persistence
- **Caching Layer** - Redis for improved performance
- **Monitoring Dashboard** - Real-time system monitoring
- **CI/CD Pipeline** - Automated testing and deployment

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

### **Development Setup**
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Your Name**
- **GitHub**: [@yourusername](https://github.com/yourusername)
- **LinkedIn**: [Your LinkedIn Profile](https://linkedin.com/in/yourprofile)
- **Email**: your.email@example.com

## 🙏 Acknowledgments

- **Dataset**: Car price dataset from Kaggle
- **Icons**: Font Awesome for beautiful icons
- **Styling**: Bootstrap for responsive design
- **ML Library**: scikit-learn for machine learning capabilities

---

⭐ **Star this repository if you found it helpful!**

📧 **Contact me for collaboration opportunities or questions about this project.**
