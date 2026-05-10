"""
Database module for SQL Injection Detection System
Handles MySQL connection, schema creation, and database operations
Uses parameterized queries to prevent SQL injection
"""

import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class DatabaseConnection:
    """Manages MySQL database connections and operations"""
    
    def __init__(self):
        """Initialize database connection parameters from environment variables"""
        self.host = os.getenv('DB_HOST', 'localhost')
        self.user = os.getenv('DB_USER', 'root')
        self.password = os.getenv('DB_PASSWORD', '')
        self.database = os.getenv('DB_NAME', 'sqli_detection')
        self.connection = None
    
    def connect(self):
        """Establish connection to MySQL database"""
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                autocommit=True
            )
            if self.connection.is_connected():
                print(f"✓ Connected to MySQL database: {self.database}")
                return True
        except Error as e:
            print(f"✗ Error connecting to MySQL: {e}")
            return False
        return False
    
    def connect_without_db(self):
        """Connect to MySQL server without specifying database (for database creation)"""
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password
            )
            if self.connection.is_connected():
                return True
        except Error as e:
            print(f"✗ Error connecting to MySQL server: {e}")
            return False
        return False
    
    def create_database(self):
        """Create the database if it doesn't exist"""
        if self.connect_without_db():
            try:
                cursor = self.connection.cursor()
                cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.database}")
                print(f"✓ Database '{self.database}' created or already exists")
                cursor.close()
                return True
            except Error as e:
                print(f"✗ Error creating database: {e}")
                return False
            finally:
                self.close()
        return False
    
    def create_tables(self):
        """Create required tables if they don't exist"""
        if self.connect():
            try:
                cursor = self.connection.cursor()
                
                # Create users table
                create_users_table = """
                CREATE TABLE IF NOT EXISTS users (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    username VARCHAR(50) UNIQUE NOT NULL,
                    password VARCHAR(255) NOT NULL,
                    role ENUM('admin', 'user') DEFAULT 'user',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """
                cursor.execute(create_users_table)
                print("✓ Users table created or already exists")
                
                # Create logs table
                create_logs_table = """
                CREATE TABLE IF NOT EXISTS logs (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    query TEXT NOT NULL,
                    detected_attack BOOLEAN NOT NULL,
                    severity ENUM('Low', 'Medium', 'High') DEFAULT 'Low',
                    attack_type VARCHAR(100),
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """
                cursor.execute(create_logs_table)
                print("✓ Logs table created or already exists")
                
                cursor.close()
                return True
                
            except Error as e:
                print(f"✗ Error creating tables: {e}")
                return False
            finally:
                self.close()
        return False
    
    def insert_user(self, username, password, role='user'):
        """
        Insert a new user into the database
        Uses parameterized query to prevent SQL injection
        """
        if self.connect():
            try:
                cursor = self.connection.cursor()
                query = "INSERT INTO users (username, password, role) VALUES (%s, %s, %s)"
                values = (username, password, role)
                cursor.execute(query, values)
                user_id = cursor.lastrowid
                print(f"✓ User '{username}' created with ID: {user_id}")
                return user_id
            except Error as e:
                if e.errno == 1062:  # Duplicate entry
                    print(f"✗ Username '{username}' already exists")
                else:
                    print(f"✗ Error inserting user: {e}")
                return None
            finally:
                cursor.close()
                self.close()
        return None
    
    def authenticate_user(self, username, password):
        """
        Authenticate user with username and password
        Uses parameterized query to prevent SQL injection
        """
        if self.connect():
            try:
                cursor = self.connection.cursor(dictionary=True)
                # Parameterized query - prevents SQL injection
                query = "SELECT id, username, role FROM users WHERE username = %s AND password = %s"
                cursor.execute(query, (username, password))
                user = cursor.fetchone()
                
                if user:
                    print(f"✓ User '{username}' authenticated successfully")
                    return user
                else:
                    print(f"✗ Authentication failed for user '{username}'")
                    return None
            except Error as e:
                print(f"✗ Error during authentication: {e}")
                return None
            finally:
                cursor.close()
                self.close()
        return None
    
    def insert_log(self, query, detected_attack, severity='Low', attack_type=None):
        """
        Insert a detection log entry
        Uses parameterized query to prevent SQL injection
        """
        if self.connect():
            try:
                cursor = self.connection.cursor()
                sql_query = """
                    INSERT INTO logs (query, detected_attack, severity, attack_type) 
                    VALUES (%s, %s, %s, %s)
                """
                values = (query, detected_attack, severity, attack_type)
                cursor.execute(sql_query, values)
                log_id = cursor.lastrowid
                return log_id
            except Error as e:
                print(f"✗ Error inserting log: {e}")
                return None
            finally:
                cursor.close()
                self.close()
        return None
    
    def get_logs(self, limit=100, user_role='user'):
        """
        Retrieve detection logs
        Admin can see all logs, regular users see limited logs
        """
        if self.connect():
            try:
                cursor = self.connection.cursor(dictionary=True)
                
                if user_role == 'admin':
                    # Admin sees all logs with limit
                    query = "SELECT * FROM logs ORDER BY timestamp DESC LIMIT %s"
                    cursor.execute(query, (limit,))
                else:
                    # Regular users see last 20 logs
                    query = "SELECT * FROM logs ORDER BY timestamp DESC LIMIT 20"
                    cursor.execute(query)
                
                logs = cursor.fetchall()
                return logs
            except Error as e:
                print(f"✗ Error retrieving logs: {e}")
                return []
            finally:
                cursor.close()
                self.close()
        return []
    
    def get_dashboard_stats(self):
        """Get statistics for dashboard visualization"""
        if self.connect():
            try:
                cursor = self.connection.cursor(dictionary=True)
                
                # Total queries tested
                cursor.execute("SELECT COUNT(*) as total FROM logs")
                total = cursor.fetchone()['total']
                
                # Total attacks detected
                cursor.execute("SELECT COUNT(*) as attacks FROM logs WHERE detected_attack = TRUE")
                attacks = cursor.fetchone()['attacks']
                
                # Severity breakdown
                cursor.execute("""
                    SELECT 
                        SUM(CASE WHEN severity = 'High' THEN 1 ELSE 0 END) as high,
                        SUM(CASE WHEN severity = 'Medium' THEN 1 ELSE 0 END) as medium,
                        SUM(CASE WHEN severity = 'Low' THEN 1 ELSE 0 END) as low
                    FROM logs WHERE detected_attack = TRUE
                """)
                severity = cursor.fetchone()
                
                # Attack types distribution
                cursor.execute("""
                    SELECT attack_type, COUNT(*) as count 
                    FROM logs 
                    WHERE detected_attack = TRUE AND attack_type IS NOT NULL
                    GROUP BY attack_type 
                    ORDER BY count DESC
                    LIMIT 10
                """)
                attack_types = cursor.fetchall()
                
                # Recent attacks (last 10)
                cursor.execute("""
                    SELECT * FROM logs 
                    WHERE detected_attack = TRUE 
                    ORDER BY timestamp DESC 
                    LIMIT 10
                """)
                recent_attacks = cursor.fetchall()
                
                return {
                    'total_queries': total,
                    'total_attacks': attacks,
                    'safe_queries': total - attacks,
                    'severity': {
                        'high': severity['high'] or 0,
                        'medium': severity['medium'] or 0,
                        'low': severity['low'] or 0
                    },
                    'attack_types': attack_types,
                    'recent_attacks': recent_attacks
                }
                
            except Error as e:
                print(f"✗ Error retrieving dashboard stats: {e}")
                return {}
            finally:
                cursor.close()
                self.close()
        return {}
    
    def close(self):
        """Close database connection"""
        if self.connection and self.connection.is_connected():
            self.connection.close()


# Initialize database instance
db = DatabaseConnection()
