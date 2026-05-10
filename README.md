# SQL Injection Detection System

A comprehensive full-stack web application that detects, logs, and prevents SQL Injection attacks using both rule-based and machine learning approaches. Built as a professional engineering final-year project.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![React](https://img.shields.io/badge/React-18.2-61DAFB.svg)
![Flask](https://img.shields.io/badge/Flask-3.0-000000.svg)
![MySQL](https://img.shields.io/badge/MySQL-8.0-4479A1.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

---

## 📋 Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation & Setup](#installation--setup)
- [Running the Application](#running-the-application)
- [API Documentation](#api-documentation)
- [ML Model Training](#ml-model-training)
- [Usage Examples](#usage-examples)
- [Security Features](#security-features)
- [Screenshots](#screenshots)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

---

## ✨ Features

### Core Functionality
- **Real-time SQL Injection Detection** - Analyze SQL queries instantly
- **Dual Detection Engine** - Rule-based + Machine Learning approaches
- **Interactive Dashboard** - Visual statistics with charts and graphs
- **Comprehensive Logging** - Track all detected attacks with severity levels
- **User Authentication** - Secure login/register system
- **Role-based Access Control** - Admin and user roles

### Detection Capabilities
- ✅ Tautology attacks (`' OR 1=1 --`)
- ✅ UNION-based injection
- ✅ Stacked queries (`; DROP TABLE`)
- ✅ Comment-based injection (`--`, `#`, `/* */`)
- ✅ Time-based injection (`WAITFOR DELAY`, `SLEEP`)
- ✅ Error-based injection
- ✅ Schema enumeration attempts
- ✅ Privilege escalation attacks
- ✅ And 20+ other attack patterns

### Advanced Features
- **ML-powered Detection** - Random Forest Classifier with TF-IDF vectorization
- **Severity Classification** - Low, Medium, High severity levels
- **Attack Type Identification** - Specific attack pattern recognition
- **Security Best Practices Demo** - Vulnerable vs secure code comparison
- **CSV Export** - Export logs for further analysis
- **Real-time Filtering** - Search and filter logs by severity

---

## 🛠 Tech Stack

### Backend
- **Python Flask** - REST API framework
- **MySQL** - Database for users and logs
- **scikit-learn** - Machine learning model
- **pandas & numpy** - Data processing
- **TF-IDF Vectorizer** - Text feature extraction
- **Random Forest Classifier** - ML algorithm

### Frontend
- **React.js 18** - UI framework
- **Tailwind CSS** - Modern styling
- **Chart.js** - Data visualization
- **Axios** - HTTP client
- **React Router** - Navigation

---

## 📁 Project Structure

```
CESH_TA3_2026/
├── backend/
│   ├── app.py                    # Flask REST API
│   ├── database.py               # MySQL connection & operations
│   ├── detection_engine.py       # Rule-based + ML detection
│   ├── ml_model.py               # ML model training & prediction
│   ├── requirements.txt          # Python dependencies
│   └── .env                      # Environment variables
│
├── frontend/
│   ├── package.json              # Node.js dependencies
│   ├── tailwind.config.js        # Tailwind configuration
│   ├── postcss.config.js         # PostCSS configuration
│   ├── public/
│   │   └── index.html            # HTML template
│   └── src/
│       ├── App.js                # Main React component
│       ├── index.js              # React entry point
│       ├── index.css             # Global styles
│       ├── components/
│       │   ├── Navbar.js         # Navigation bar
│       │   ├── Login.js          # Login form
│       │   ├── Register.js       # Registration form
│       │   ├── Dashboard.js      # Statistics dashboard
│       │   ├── QueryTester.js    # Query testing interface
│       │   └── LogsViewer.js     # Logs management (admin)
│       └── services/
│           └── api.js            # API service layer
│
├── dataset/
│   └── sqli_dataset.csv          # ML training dataset (286 samples)
│
├── train_model.py                # Standalone ML training script
└── README.md                     # This file
```

---

## 📦 Prerequisites

Before installation, ensure you have:

- **Python 3.8 or higher** - [Download Python](https://www.python.org/downloads/)
- **Node.js 16+ and npm** - [Download Node.js](https://nodejs.org/)
- **MySQL 8.0+** - [Download MySQL](https://dev.mysql.com/downloads/)
- **Git** - [Download Git](https://git-scm.com/)

---

## 🚀 Installation & Setup

### Step 1: Clone the Repository

```bash
git clone <repository-url>
cd CESH_TA3_2026
```

### Step 2: Setup MySQL Database

1. **Start MySQL Server**

2. **Create Database** (Optional - the app will create it automatically)
```sql
CREATE DATABASE sqli_detection;
```

3. **Note your MySQL credentials** - You'll need:
   - Host (usually `localhost`)
   - Username (usually `root`)
   - Password (your MySQL password)

### Step 3: Setup Backend

```bash
# Navigate to backend directory
cd backend

# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt

# Configure environment variables
# Edit .env file with your MySQL credentials
```

**Edit `backend/.env`:**
```env
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_NAME=sqli_detection
FLASK_SECRET_KEY=your_secret_key_here
```

### Step 4: Train ML Model

```bash
# From project root directory
python train_model.py
```

This will:
- Load the dataset from `dataset/sqli_dataset.csv`
- Train the Random Forest model
- Save the model to `backend/sqli_model.pkl`
- Display accuracy and feature importance

### Step 5: Setup Frontend

```bash
# Navigate to frontend directory
cd frontend

# Install Node.js dependencies
npm install
```

---

## 🏃 Running the Application

### Option 1: Run Backend and Frontend Separately

**Terminal 1 - Backend:**
```bash
cd backend
# Activate virtual environment if not already activated
venv\Scripts\activate  # Windows
# or
source venv/bin/activate  # Linux/Mac

# Start Flask server
python app.py
```

Backend will start at: **http://localhost:5000**

**Terminal 2 - Frontend:**
```bash
cd frontend

# Start React development server
npm start
```

Frontend will start at: **http://localhost:3000**

### Option 2: Access the Application

Once both servers are running:
- **Frontend UI**: http://localhost:3000
- **Backend API**: http://localhost:5000/api

---

## 📡 API Documentation

### Base URL
```
http://localhost:5000/api
```

### Endpoints

#### 1. Register User
```http
POST /api/register
Content-Type: application/json

{
  "username": "testuser",
  "password": "password123"
}
```

**Response:**
```json
{
  "success": true,
  "message": "User registered successfully",
  "user_id": 1
}
```

#### 2. Login
```http
POST /api/login
Content-Type: application/json

{
  "username": "testuser",
  "password": "password123"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Login successful",
  "token": "uuid-token-here",
  "user": {
    "id": 1,
    "username": "testuser",
    "role": "user"
  }
}
```

#### 3. Test SQL Query
```http
POST /api/test-query
Content-Type: application/json

{
  "query": "' OR 1=1 --",
  "user_id": 1
}
```

**Response:**
```json
{
  "success": true,
  "is_attack": true,
  "severity": "High",
  "attack_type": "Comment-based injection",
  "method": "rule-based",
  "confidence": 1.0,
  "recommendation": "Block queries containing SQL comments (--, #, /* */)",
  "blocked": true
}
```

#### 4. Get Logs
```http
GET /api/logs?limit=100&role=admin
```

**Response:**
```json
{
  "success": true,
  "logs": [
    {
      "id": 1,
      "query": "' OR 1=1 --",
      "detected_attack": true,
      "severity": "High",
      "attack_type": "Comment-based injection",
      "timestamp": "2024-01-15T10:30:00"
    }
  ],
  "count": 1
}
```

#### 5. Get Dashboard Statistics
```http
GET /api/dashboard-stats
```

**Response:**
```json
{
  "success": true,
  "stats": {
    "total_queries": 150,
    "total_attacks": 45,
    "safe_queries": 105,
    "severity": {
      "high": 20,
      "medium": 15,
      "low": 10
    },
    "attack_types": [...],
    "recent_attacks": [...]
  }
}
```

#### 6. Health Check
```http
GET /api/health
```

---

## 🤖 ML Model Training

### Dataset

The training dataset (`dataset/sqli_dataset.csv`) contains:
- **286 SQL queries** total
- **143 safe queries** (label: 0)
- **143 malicious queries** (label: 1)

### Model Architecture

- **Algorithm**: Random Forest Classifier
- **Feature Extraction**: TF-IDF Vectorizer (character-level n-grams)
- **Parameters**:
  - n_estimators: 100
  - max_depth: 20
  - min_samples_split: 5
  - ngram_range: (1, 3)
  - analyzer: char_wb

### Retraining the Model

```bash
python train_model.py
```

The model will be saved to `backend/sqli_model.pkl`

### Expected Performance

- **Accuracy**: ~95-98%
- **Precision**: High (low false positives)
- **Recall**: High (catches most attacks)

---

## 💡 Usage Examples

### Example 1: Testing a Safe Query

**Input:**
```sql
SELECT * FROM users WHERE id = 1
```

**Result:**
```
✓ Query Appears Safe
Detection Method: machine-learning
Confidence: 94.2%
Recommendation: Query appears safe
```

### Example 2: Testing a Malicious Query

**Input:**
```sql
' OR 1=1 --
```

**Result:**
```
✗ SQL Injection Detected!
Detection Method: rule-based
Confidence: 100%
Attack Type: Comment-based injection
Severity: High
Recommendation: Block queries containing SQL comments (--, #, /* */)
```

### Example 3: Testing UNION-based Attack

**Input:**
```sql
' UNION SELECT username, password FROM users --
```

**Result:**
```
✗ SQL Injection Detected!
Detection Method: rule-based
Confidence: 100%
Attack Type: UNION-based injection
Severity: High
Recommendation: Use parameterized queries and validate input types
```

---

## 🔒 Security Features

### Implemented Security Measures

1. **Parameterized Queries** - All database operations use prepared statements
2. **Password Hashing** - SHA-256 hashing (upgrade to bcrypt for production)
3. **Token-based Authentication** - UUID tokens for session management
4. **Input Validation** - Server-side validation for all inputs
5. **CORS Configuration** - Controlled access to API endpoints
6. **Role-based Access Control** - Admin vs user permissions
7. **SQL Injection Prevention** - The system itself is protected against SQLi

### Security Best Practices Demonstrated

The application includes a **Security Comparison Demo** showing:
- ❌ Vulnerable code (string concatenation)
- ✅ Secure code (parameterized queries)
- Key security tips for developers

---

## 📸 Screenshots

### Login Page
Modern authentication interface with gradient background

### Dashboard
- Statistics cards (Total Queries, Attacks, Safe, Attack Rate)
- Severity distribution pie chart
- Top attack types list
- Recent attacks table

### Query Tester
- Real-time query analysis
- Safe and malicious example queries
- Security best practices comparison
- Common attack types reference

### Logs Viewer (Admin)
- Comprehensive log table
- Search and filter functionality
- CSV export capability
- Pagination support

---

## 🔧 Troubleshooting

### Issue: MySQL Connection Error

**Solution:**
1. Verify MySQL is running
2. Check credentials in `backend/.env`
3. Ensure database exists: `CREATE DATABASE sqli_detection;`

### Issue: ML Model Not Found

**Solution:**
```bash
python train_model.py
```

### Issue: CORS Error in Frontend

**Solution:**
- Ensure backend is running on `http://localhost:5000`
- Check that `flask-cors` is installed

### Issue: Frontend Won't Start

**Solution:**
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
npm start
```

### Issue: Port Already in Use

**Backend:**
```bash
# Change port in backend/app.py
app.run(debug=True, host='0.0.0.0', port=5001)
```

**Frontend:**
```bash
# Frontend will automatically use port 3001 if 3000 is busy
```

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 👨‍💻 Developer

**SQL Injection Detection System**  
Built as an engineering final-year project  
Demonstrates full-stack development, machine learning, and cybersecurity concepts

---

## 🙏 Acknowledgments

- OWASP for SQL injection prevention guidelines
- scikit-learn documentation for ML implementation
- React and Flask communities for excellent documentation

---

## 📞 Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Check the Troubleshooting section above
- Review API documentation for endpoint details

---

**Happy Detecting! 🔍🛡️**
