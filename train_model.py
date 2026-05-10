"""
Standalone ML Model Training Script
Run this script to train the SQL injection detection model

Usage:
    python train_model.py
"""

import sys
import os

# Add parent directory to path to import backend modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from backend.ml_model import ml_model


def main():
    """Train the SQL injection detection model"""
    
    print("\n" + "="*70)
    print("SQL INJECTION DETECTION MODEL - TRAINING SCRIPT")
    print("="*70)
    
    # Check if dataset exists
    dataset_path = 'dataset/sqli_dataset.csv'
    if not os.path.exists(dataset_path):
        print(f"\n✗ Error: Dataset file not found at '{dataset_path}'")
        print("  Please ensure the dataset file exists before training.")
        return False
    
    print(f"\n✓ Dataset found: {dataset_path}")
    
    # Train the model
    success = ml_model.train_model(dataset_path)
    
    if success:
        print("\n" + "="*70)
        print("TRAINING COMPLETE")
        print("="*70)
        
        # Display feature importance
        print("\nTop 20 Most Important Features for Detection:")
        print("-" * 70)
        
        feature_importance = ml_model.get_feature_importance(top_n=20)
        for i, (feature, importance) in enumerate(feature_importance, 1):
            print(f"{i:2d}. {feature:<40} {importance:.4f}")
        
        print("\n" + "="*70)
        print("Model saved to: backend/sqli_model.pkl")
        print("Ready to use in the detection engine!")
        print("="*70 + "\n")
        
        return True
    else:
        print("\n✗ Training failed. Please check the errors above.")
        return False


if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
