"""
Flask REST API for SQL Injection Detection System
Provides endpoints for authentication, query testing, and log management
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import hashlib
import uuid

from database import db
from detection_engine import detection_engine

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'sqli-detection-system-secret-key-2024'

# Enable CORS for React frontend
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Simple token storage (in production, use JWT or database)
active_tokens = {}


def hash_password(password):
    """Hash password using SHA-256 (for demo purposes - use bcrypt in production)"""
    return hashlib.sha256(password.encode()).hexdigest()


def generate_token():
    """Generate unique authentication token"""
    return str(uuid.uuid4())


@app.route('/api/register', methods=['POST'])
def register():
    """
    Register a new user
    
    Request body:
    {
        "username": "string",
        "password": "string"
    }
    
    Response:
    {
        "success": bool,
        "message": "string",
        "user_id": int (optional)
    }
    """
    try:
        data = request.get_json()
        
        # Validate input
        if not data or 'username' not in data or 'password' not in data:
            return jsonify({
                'success': False,
                'message': 'Username and password are required'
            }), 400
        
        username = data['username'].strip()
        password = data['password'].strip()
        
        if len(username) < 3 or len(username) > 50:
            return jsonify({
                'success': False,
                'message': 'Username must be between 3 and 50 characters'
            }), 400
        
        if len(password) < 6:
            return jsonify({
                'success': False,
                'message': 'Password must be at least 6 characters'
            }), 400
        
        # Hash password
        hashed_password = hash_password(password)
        
        # Insert user into database
        user_id = db.insert_user(username, hashed_password, role='user')
        
        if user_id:
            return jsonify({
                'success': True,
                'message': 'User registered successfully',
                'user_id': user_id
            }), 201
        else:
            return jsonify({
                'success': False,
                'message': 'Username already exists or registration failed'
            }), 400
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Registration error: {str(e)}'
        }), 500


@app.route('/api/login', methods=['POST'])
def login():
    """
    Authenticate user and return token
    
    Request body:
    {
        "username": "string",
        "password": "string"
    }
    
    Response:
    {
        "success": bool,
        "message": "string",
        "token": "string" (optional),
        "user": {
            "id": int,
            "username": "string",
            "role": "string"
        } (optional)
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'username' not in data or 'password' not in data:
            return jsonify({
                'success': False,
                'message': 'Username and password are required'
            }), 400
        
        username = data['username'].strip()
        password = data['password'].strip()
        
        # Hash password and authenticate
        hashed_password = hash_password(password)
        user = db.authenticate_user(username, hashed_password)
        
        if user:
            # Generate authentication token
            token = generate_token()
            
            # Store token (in production, use JWT with expiration)
            active_tokens[token] = {
                'user_id': user['id'],
                'username': user['username'],
                'role': user['role'],
                'login_time': datetime.now().isoformat()
            }
            
            return jsonify({
                'success': True,
                'message': 'Login successful',
                'token': token,
                'user': {
                    'id': user['id'],
                    'username': user['username'],
                    'role': user['role']
                }
            }), 200
        else:
            return jsonify({
                'success': False,
                'message': 'Invalid username or password'
            }), 401
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Login error: {str(e)}'
        }), 500


@app.route('/api/test-query', methods=['POST'])
def test_query():
    """
    Test a SQL query for injection attacks
    
    Request body:
    {
        "query": "string",
        "user_id": int (optional)
    }
    
    Response:
    {
        "success": bool,
        "is_attack": bool,
        "severity": "string",
        "attack_type": "string",
        "method": "string",
        "confidence": float,
        "recommendation": "string",
        "blocked": bool
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'query' not in data:
            return jsonify({
                'success': False,
                'message': 'Query is required'
            }), 400
        
        query = data['query'].strip()
        
        if not query:
            return jsonify({
                'success': False,
                'message': 'Query cannot be empty'
            }), 400
        
        # Analyze query using detection engine
        result = detection_engine.analyze_query(query)
        
        # Log the detection result
        db.insert_log(
            query=query,
            detected_attack=result['is_attack'],
            severity=result['severity'],
            attack_type=result.get('attack_type')
        )
        
        return jsonify({
            'success': True,
            **result
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Query testing error: {str(e)}'
        }), 500


@app.route('/api/logs', methods=['GET'])
def get_logs():
    """
    Get detection logs
    
    Query parameters:
    - limit: int (default: 100)
    - role: string (admin/user)
    
    Response:
    {
        "success": bool,
        "logs": [array of log objects],
        "count": int
    }
    """
    try:
        limit = request.args.get('limit', 100, type=int)
        role = request.args.get('role', 'user')
        
        # Retrieve logs from database
        logs = db.get_logs(limit=limit, user_role=role)
        
        return jsonify({
            'success': True,
            'logs': logs,
            'count': len(logs)
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error retrieving logs: {str(e)}'
        }), 500


@app.route('/api/dashboard-stats', methods=['GET'])
def get_dashboard_stats():
    """
    Get dashboard statistics
    
    Response:
    {
        "success": bool,
        "stats": {
            "total_queries": int,
            "total_attacks": int,
            "safe_queries": int,
            "severity": {
                "high": int,
                "medium": int,
                "low": int
            },
            "attack_types": [array],
            "recent_attacks": [array]
        }
    }
    """
    try:
        stats = db.get_dashboard_stats()
        
        return jsonify({
            'success': True,
            'stats': stats
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error retrieving dashboard stats: {str(e)}'
        }), 500


@app.route('/api/logout', methods=['POST'])
def logout():
    """
    Logout user and invalidate token
    
    Request headers:
    - Authorization: Bearer <token>
    
    Response:
    {
        "success": bool,
        "message": "string"
    }
    """
    try:
        token = request.headers.get('Authorization', '').replace('Bearer ', '')
        
        if token in active_tokens:
            del active_tokens[token]
            return jsonify({
                'success': True,
                'message': 'Logged out successfully'
            }), 200
        else:
            return jsonify({
                'success': False,
                'message': 'Invalid token'
            }), 401
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Logout error: {str(e)}'
        }), 500


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'SQL Injection Detection System',
        'timestamp': datetime.now().isoformat()
    }), 200


# Initialize database tables on startup
with app.app_context():
    print("\n" + "="*60)
    print("SQL INJECTION DETECTION SYSTEM - STARTING UP")
    print("="*60)
    
    # Create database and tables
    db.create_database()
    db.create_tables()
    
    print("\n✓ Database initialization complete")
    print("="*60 + "\n")


if __name__ == '__main__':
    print("\n🚀 Starting Flask API Server...")
    print("📡 API available at: http://localhost:5000")
    print("🔌 Frontend should connect to: http://localhost:5000/api")
    print("\n" + "="*60)
    
    app.run(debug=True, host='0.0.0.0', port=5000)
