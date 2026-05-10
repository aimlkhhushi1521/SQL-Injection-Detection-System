"""
Model Evaluation Script for SQL Injection Detection
Evaluates the trained model using various metrics and generates visualization graphs

Usage:
    python evaluate_model.py
"""

import sys
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, classification_report, roc_curve, auc,
    precision_recall_curve, average_precision_score
)
import joblib

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from backend.ml_model import SQLInjectionMLModel


def load_evaluation_data(dataset_path='dataset/sqli_dataset.csv'):
    """Load dataset for evaluation"""
    df = pd.read_csv(dataset_path)
    queries = df['query'].astype(str).tolist()
    labels = df['label'].astype(int).tolist()
    return queries, labels


def evaluate_model(model, X_test, y_test, y_pred, y_pred_proba):
    """Calculate all evaluation metrics"""
    
    metrics = {
        'accuracy': accuracy_score(y_test, y_pred),
        'precision': precision_score(y_test, y_pred),
        'recall': recall_score(y_test, y_pred),
        'f1_score': f1_score(y_test, y_pred),
        'precision_malicious': precision_score(y_test, y_pred, pos_label=1),
        'recall_malicious': recall_score(y_test, y_pred, pos_label=1),
        'f1_malicious': f1_score(y_test, y_pred, pos_label=1),
    }
    
    # Calculate ROC-AUC
    fpr, tpr, _ = roc_curve(y_test, y_pred_proba[:, 1])
    metrics['auc_roc'] = auc(fpr, tpr)
    metrics['fpr'] = fpr
    metrics['tpr'] = tpr
    
    # Calculate Precision-Recall curve
    precision_curve, recall_curve, _ = precision_recall_curve(y_test, y_pred_proba[:, 1])
    metrics['avg_precision'] = average_precision_score(y_test, y_pred_proba[:, 1])
    metrics['precision_curve'] = precision_curve
    metrics['recall_curve'] = recall_curve
    
    # Confusion matrix
    metrics['confusion_matrix'] = confusion_matrix(y_test, y_pred)
    
    # Classification report
    metrics['classification_report'] = classification_report(
        y_test, y_pred, target_names=['Safe', 'Malicious'], output_dict=True
    )
    
    return metrics


def plot_confusion_matrix(cm, save_path='backend/evaluation_results/confusion_matrix.png'):
    """Plot and save confusion matrix heatmap"""
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                xticklabels=['Safe', 'Malicious'],
                yticklabels=['Safe', 'Malicious'],
                annot_kws={'size': 16})
    plt.title('Confusion Matrix', fontsize=14, fontweight='bold')
    plt.xlabel('Predicted Label', fontsize=12)
    plt.ylabel('True Label', fontsize=12)
    plt.tight_layout()
    plt.savefig(save_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"✓ Saved: {save_path}")


def plot_roc_curve(fpr, tpr, auc_score, save_path='backend/evaluation_results/roc_curve.png'):
    """Plot and save ROC curve"""
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    
    plt.figure(figsize=(8, 6))
    plt.plot(fpr, tpr, color='darkorange', lw=2, 
             label=f'ROC curve (AUC = {auc_score:.4f})')
    plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--', label='Random Classifier')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate', fontsize=12)
    plt.ylabel('True Positive Rate', fontsize=12)
    plt.title('Receiver Operating Characteristic (ROC) Curve', fontsize=14, fontweight='bold')
    plt.legend(loc='lower right', fontsize=11)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(save_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"✓ Saved: {save_path}")


def plot_precision_recall_curve(precision_curve, recall_curve, avg_precision, 
                                 save_path='backend/evaluation_results/precision_recall_curve.png'):
    """Plot and save Precision-Recall curve"""
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    
    plt.figure(figsize=(8, 6))
    plt.plot(recall_curve, precision_curve, color='green', lw=2,
             label=f'Precision-Recall curve (AP = {avg_precision:.4f})')
    plt.xlabel('Recall', fontsize=12)
    plt.ylabel('Precision', fontsize=12)
    plt.title('Precision-Recall Curve', fontsize=14, fontweight='bold')
    plt.legend(loc='lower left', fontsize=11)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(save_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"✓ Saved: {save_path}")


def plot_metrics_bar(metrics, save_path='backend/evaluation_results/metrics_bar.png'):
    """Plot and save metrics bar chart"""
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    
    metric_names = ['Accuracy', 'Precision', 'Recall', 'F1-Score', 'AUC-ROC']
    metric_values = [
        metrics['accuracy'],
        metrics['precision'],
        metrics['recall'],
        metrics['f1_score'],
        metrics['auc_roc']
    ]
    
    plt.figure(figsize=(10, 6))
    bars = plt.bar(metric_names, metric_values, color=['#3498db', '#2ecc71', '#e74c3c', '#9b59b6', '#f39c12'])
    
    # Add value labels on bars
    for bar, value in zip(bars, metric_values):
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height + 0.01,
                f'{value:.4f}', ha='center', va='bottom', fontsize=12, fontweight='bold')
    
    plt.ylim(0, 1.15)
    plt.ylabel('Score', fontsize=12)
    plt.title('Model Performance Metrics', fontsize=14, fontweight='bold')
    plt.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    plt.savefig(save_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"✓ Saved: {save_path}")


def plot_class_distribution(queries, labels, save_path='backend/evaluation_results/class_distribution.png'):
    """Plot class distribution"""
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    
    safe_count = labels.count(0)
    malicious_count = labels.count(1)
    
    plt.figure(figsize=(8, 6))
    colors = ['#2ecc71', '#e74c3c']
    bars = plt.bar(['Safe (0)', 'Malicious (1)'], [safe_count, malicious_count], color=colors)
    
    for bar, count in zip(bars, [safe_count, malicious_count]):
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height + 50,
                f'{count}', ha='center', va='bottom', fontsize=14, fontweight='bold')
    
    plt.ylabel('Number of Samples', fontsize=12)
    plt.title('Dataset Class Distribution', fontsize=14, fontweight='bold')
    plt.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    plt.savefig(save_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"✓ Saved: {save_path}")


def plot_feature_importance(model, vectorizer, save_path='backend/evaluation_results/feature_importance.png'):
    """Plot top feature importances"""
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    
    feature_importance = model.feature_importances_
    feature_names = vectorizer.get_feature_names_out()
    
    # Get top 20 features
    top_n = 20
    top_indices = np.argsort(feature_importance)[-top_n:]
    top_features = [feature_names[i] for i in top_indices]
    top_importance = feature_importance[top_indices]
    
    plt.figure(figsize=(12, 8))
    colors = plt.cm.RdYlGn(np.linspace(0.2, 0.8, top_n))
    bars = plt.barh(range(top_n), top_importance, color=colors)
    plt.yticks(range(top_n), top_features)
    plt.xlabel('Feature Importance', fontsize=12)
    plt.title('Top 20 Most Important Features for SQL Injection Detection', 
              fontsize=14, fontweight='bold')
    plt.grid(axis='x', alpha=0.3)
    plt.tight_layout()
    plt.savefig(save_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"✓ Saved: {save_path}")


def generate_evaluation_report(metrics, save_path='backend/evaluation_results/report.txt'):
    """Generate text report of evaluation results"""
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    
    report = """
================================================================================
                    SQL INJECTION DETECTION MODEL - EVALUATION REPORT
================================================================================

OVERALL METRICS
---------------
Accuracy          : {:.4f} ({:.2f}%)
Precision         : {:.4f}
Recall            : {:.4f}
F1-Score          : {:.4f}
AUC-ROC           : {:.4f}
Average Precision : {:.4f}

CLASS-SPECIFIC METRICS
-----------------------
Safe Queries (Label 0):
  - Precision : {:.4f}
  - Recall    : {:.4f}
  - F1-Score  : {:.4f}

Malicious Queries (Label 1):
  - Precision : {:.4f}
  - Recall    : {:.4f}
  - F1-Score  : {:.4f}

CONFUSION MATRIX
----------------
                  Predicted
                  Safe    Malicious
Actual  Safe      {:5d}    {:5d}
        Malicious{:5d}    {:5d}

INTERPRETATION
--------------
- True Negatives (TN)  : {:5d} - Correctly identified safe queries
- False Positives (FP) : {:5d} - Safe queries incorrectly flagged as malicious
- False Negatives (FN) : {:5d} - Malicious queries missed (not detected)
- True Positives (TP)  : {:5d} - Correctly identified malicious queries

GENERATED VISUALIZATIONS
------------------------
1. confusion_matrix.png    - Heatmap of confusion matrix
2. roc_curve.png          - ROC curve with AUC score
3. precision_recall_curve.png - Precision-Recall curve
4. metrics_bar.png        - Bar chart of all metrics
5. class_distribution.png  - Dataset class distribution
6. feature_importance.png - Top 20 important features

================================================================================
""".format(
        metrics['accuracy'], metrics['accuracy'] * 100,
        metrics['precision'], metrics['recall'], metrics['f1_score'],
        metrics['auc_roc'], metrics['avg_precision'],
        metrics['classification_report']['Safe']['precision'],
        metrics['classification_report']['Safe']['recall'],
        metrics['classification_report']['Safe']['f1-score'],
        metrics['classification_report']['Malicious']['precision'],
        metrics['classification_report']['Malicious']['recall'],
        metrics['classification_report']['Malicious']['f1-score'],
        metrics['confusion_matrix'][0][0], metrics['confusion_matrix'][0][1],
        metrics['confusion_matrix'][1][0], metrics['confusion_matrix'][1][1],
        metrics['confusion_matrix'][0][0],
        metrics['confusion_matrix'][0][1],
        metrics['confusion_matrix'][1][0],
        metrics['confusion_matrix'][1][1]
    )
    
    with open(save_path, 'w') as f:
        f.write(report)
    
    print(f"✓ Saved: {save_path}")
    return report


def main():
    """Main evaluation function"""
    
    print("\n" + "="*70)
    print("SQL INJECTION DETECTION MODEL - EVALUATION")
    print("="*70)
    
    # Initialize model
    model = SQLInjectionMLModel()
    
    # Check if trained model exists
    model_path = 'backend/sqli_model.pkl'
    if not os.path.exists(model_path):
        print(f"\n✗ Trained model not found at '{model_path}'")
        print("  Please train the model first using: python train_model.py")
        return False
    
    # Load trained model
    print("\nLoading trained model...")
    model.load_model()
    
    # Load dataset
    print("Loading dataset for evaluation...")
    queries, labels = load_evaluation_data()
    print(f"✓ Loaded {len(queries)} samples")
    
    # Split data (same as training)
    X_train, X_test, y_train, y_test = train_test_split(
        queries, labels, test_size=0.2, random_state=42, stratify=labels
    )
    
    # Transform test data
    X_test_tfidf = model.vectorizer.transform(X_test)
    
    # Make predictions
    print("Making predictions on test set...")
    y_pred = model.model.predict(X_test_tfidf)
    y_pred_proba = model.model.predict_proba(X_test_tfidf)
    
    # Calculate metrics
    print("\nCalculating evaluation metrics...")
    metrics = evaluate_model(model.model, X_test_tfidf, y_test, y_pred, y_pred_proba)
    
    # Print metrics to console
    print("\n" + "="*70)
    print("EVALUATION RESULTS")
    print("="*70)
    print(f"Accuracy          : {metrics['accuracy']:.4f}")
    print(f"Precision         : {metrics['precision']:.4f}")
    print(f"Recall            : {metrics['recall']:.4f}")
    print(f"F1-Score          : {metrics['f1_score']:.4f}")
    print(f"AUC-ROC           : {metrics['auc_roc']:.4f}")
    print(f"Average Precision : {metrics['avg_precision']:.4f}")
    
    # Generate visualizations
    print("\n" + "-"*70)
    print("Generating visualization graphs...")
    print("-"*70)
    
    plot_confusion_matrix(metrics['confusion_matrix'])
    plot_roc_curve(metrics['fpr'], metrics['tpr'], metrics['auc_roc'])
    plot_precision_recall_curve(metrics['precision_curve'], metrics['recall_curve'], 
                                 metrics['avg_precision'])
    plot_metrics_bar(metrics)
    plot_class_distribution(queries, labels)
    plot_feature_importance(model.model, model.vectorizer)
    
    # Generate text report
    print("\n" + "-"*70)
    print("Generating evaluation report...")
    print("-"*70)
    report = generate_evaluation_report(metrics)
    print(report)
    
    print("\n" + "="*70)
    print("EVALUATION COMPLETE")
    print("="*70)
    print("\nAll results saved to: backend/evaluation_results/")
    print("="*70 + "\n")
    
    return True


if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)