"""
Machine Learning Model for SQL Injection Detection
Trains a Random Forest Classifier using TF-IDF vectorization
Predicts whether a SQL query is safe or malicious
"""

import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import joblib
import os


class SQLInjectionMLModel:
    """Machine Learning model for SQL injection detection"""
    
    def __init__(self, model_path='backend/sqli_model.pkl'):
        """
        Initialize ML model components
        
        Args:
            model_path: Path to save/load the trained model
        """
        self.model_path = model_path
        self.model = None
        self.vectorizer = None
        self.is_trained = False
    
    def load_dataset(self, dataset_path='dataset/sqli_dataset.csv'):
        """
        Load training dataset from CSV file
        
        Args:
            dataset_path: Path to the CSV dataset
            
        Returns:
            tuple: (queries, labels) if successful, else (None, None)
        """
        try:
            if not os.path.exists(dataset_path):
                print(f"✗ Dataset file not found: {dataset_path}")
                return None, None
            
            # Read CSV file
            df = pd.read_csv(dataset_path)
            
            # Validate dataset structure
            if 'query' not in df.columns or 'label' not in df.columns:
                print("✗ Invalid dataset format. Required columns: 'query', 'label'")
                return None, None
            
            queries = df['query'].astype(str).tolist()
            labels = df['label'].astype(int).tolist()
            
            print(f"✓ Loaded {len(queries)} samples from dataset")
            print(f"  - Safe queries: {labels.count(0)}")
            print(f"  - Malicious queries: {labels.count(1)}")
            
            return queries, labels
            
        except Exception as e:
            print(f"✗ Error loading dataset: {e}")
            return None, None
    
    def train_model(self, dataset_path='dataset/sqli_dataset.csv'):
        """
        Train the Random Forest model on the dataset
        
        Args:
            dataset_path: Path to the training dataset
            
        Returns:
            bool: True if training successful, False otherwise
        """
        print("\n" + "="*60)
        print("TRAINING SQL INJECTION DETECTION MODEL")
        print("="*60)
        
        # Load dataset
        queries, labels = self.load_dataset(dataset_path)
        if queries is None:
            return False
        
        # Split data into training and testing sets (80% train, 20% test)
        X_train, X_test, y_train, y_test = train_test_split(
            queries, labels, test_size=0.2, random_state=42, stratify=labels
        )
        
        print(f"\nDataset split:")
        print(f"  - Training samples: {len(X_train)}")
        print(f"  - Testing samples: {len(X_test)}")
        
        # Create TF-IDF Vectorizer
        # Converts text queries to numerical features
        print("\nVectorizing queries using TF-IDF...")
        self.vectorizer = TfidfVectorizer(
            max_features=5000,
            ngram_range=(1, 3),  # Use unigrams, bigrams, and trigrams
            sublinear_tf=True,   # Apply sublinear tf scaling
            analyzer='char_wb',  # Character-level features for better SQL pattern detection
            min_df=2             # Ignore terms that appear in less than 2 documents
        )
        
        # Transform text to TF-IDF features
        X_train_tfidf = self.vectorizer.fit_transform(X_train)
        X_test_tfidf = self.vectorizer.transform(X_test)
        
        print(f"✓ Feature matrix shape: {X_train_tfidf.shape}")
        
        # Train Random Forest Classifier
        print("\nTraining Random Forest Classifier...")
        self.model = RandomForestClassifier(
            n_estimators=100,        # Number of trees
            max_depth=20,            # Maximum depth of trees
            min_samples_split=5,     # Minimum samples required to split
            min_samples_leaf=2,      # Minimum samples required at leaf
            random_state=42,
            n_jobs=-1                # Use all CPU cores
        )
        
        self.model.fit(X_train_tfidf, y_train)
        self.is_trained = True
        
        # Evaluate model performance
        print("\n" + "="*60)
        print("MODEL EVALUATION")
        print("="*60)
        
        y_pred = self.model.predict(X_test_tfidf)
        accuracy = accuracy_score(y_test, y_pred)
        
        print(f"\nAccuracy: {accuracy * 100:.2f}%")
        print("\nClassification Report:")
        print(classification_report(y_test, y_pred, target_names=['Safe', 'Malicious']))
        
        # Save model and vectorizer
        self.save_model()
        
        return True
    
    def save_model(self):
        """Save trained model and vectorizer to disk"""
        try:
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
            
            model_data = {
                'model': self.model,
                'vectorizer': self.vectorizer,
                'is_trained': self.is_trained
            }
            
            joblib.dump(model_data, self.model_path)
            print(f"\n✓ Model saved to: {self.model_path}")
            
        except Exception as e:
            print(f"✗ Error saving model: {e}")
    
    def load_model(self):
        """Load trained model and vectorizer from disk"""
        try:
            if not os.path.exists(self.model_path):
                print(f"✗ Model file not found: {self.model_path}")
                print("  Please train the model first using train_model()")
                return False
            
            model_data = joblib.load(self.model_path)
            self.model = model_data['model']
            self.vectorizer = model_data['vectorizer']
            self.is_trained = model_data['is_trained']
            
            print(f"✓ Model loaded from: {self.model_path}")
            return True
            
        except Exception as e:
            print(f"✗ Error loading model: {e}")
            return False
    
    def predict(self, query):
        """
        Predict whether a SQL query is safe or malicious
        
        Args:
            query: SQL query string to analyze
            
        Returns:
            dict: Prediction result with confidence score
        """
        if not self.is_trained or self.model is None:
            # Try to load model if not trained
            if not self.load_model():
                return {
                    'prediction': 'unknown',
                    'confidence': 0.0,
                    'error': 'Model not trained or loaded'
                }
        
        try:
            # Vectorize the query
            query_tfidf = self.vectorizer.transform([query])
            
            # Get prediction
            prediction = self.model.predict(query_tfidf)[0]
            
            # Get prediction probabilities
            probabilities = self.model.predict_proba(query_tfidf)[0]
            confidence = float(max(probabilities))
            
            # Format result
            result = {
                'prediction': 'malicious' if prediction == 1 else 'safe',
                'confidence': confidence,
                'confidence_safe': float(probabilities[0]),
                'confidence_malicious': float(probabilities[1])
            }
            
            return result
            
        except Exception as e:
            print(f"✗ Error during prediction: {e}")
            return {
                'prediction': 'unknown',
                'confidence': 0.0,
                'error': str(e)
            }
    
    def get_feature_importance(self, top_n=20):
        """
        Get top N most important features for detection
        
        Args:
            top_n: Number of top features to return
            
        Returns:
            list: Top features with importance scores
        """
        if self.model is None or self.vectorizer is None:
            print("✗ Model not trained or loaded")
            return []
        
        # Get feature importances
        importances = self.model.feature_importances_
        feature_names = self.vectorizer.get_feature_names_out()
        
        # Create list of (feature, importance) tuples
        feature_importance = list(zip(feature_names, importances))
        
        # Sort by importance (descending)
        feature_importance.sort(key=lambda x: x[1], reverse=True)
        
        # Return top N features
        return feature_importance[:top_n]


# Initialize model instance
ml_model = SQLInjectionMLModel()
