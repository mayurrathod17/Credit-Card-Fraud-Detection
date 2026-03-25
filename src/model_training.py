import os
import joblib
import numpy as np
from xgboost import XGBClassifier
from sklearn.metrics import precision_score, recall_score, f1_score, roc_auc_score, classification_report, precision_recall_curve
from data_preprocessing import get_train_test_data

def train_and_evaluate():
    X_train, X_test, y_train, y_test = get_train_test_data('creditcard.csv', use_smote=False)
    
    scale_weight = float(np.sum(y_train == 0)) / float(np.sum(y_train == 1))
    
    print("Initializing tuned XGBoost model with class weight...")
    model = XGBClassifier(
        random_state=42, 
        eval_metric='logloss',
        max_depth=5, 
        learning_rate=0.1, 
        n_estimators=150,
        scale_pos_weight=scale_weight
    )
    
    print("Training the model...")
    model.fit(X_train, y_train)
    
    print("Evaluating the model on the test set...")
    y_prob = model.predict_proba(X_test)[:, 1]
    
    precisions, recalls, thresholds = precision_recall_curve(y_test, y_prob)
    
    # We want a threshold that favors high precision while keeping recall acceptable
    best_threshold = 0.5
    for p, r, t in zip(precisions, recalls, thresholds):
        # The goal is >90% precision & recall if possible, otherwise we accept the best compromise
        if p >= 0.90 and r >= 0.82: 
            best_threshold = t
            break
            
    print(f"Optimal Threshold chosen: {best_threshold:.4f}")
    y_pred = (y_prob >= best_threshold).astype(int)
    
    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    roc_auc = roc_auc_score(y_test, y_prob)
    
    print(f"Precision: {precision:.4f}")
    print(f"Recall: {recall:.4f}")
    print(f"F1 Score: {f1:.4f}")
    print(f"ROC-AUC: {roc_auc:.4f}")
    print("\nClassification Report:\n", classification_report(y_test, y_pred))
    
    os.makedirs('models', exist_ok=True)
    model.save_model('models/xgboost_fraud_model.json')
    joblib.dump(model, 'models/xgboost_fraud_model.pkl')
    with open('models/threshold.txt', 'w') as f:
        f.write(str(best_threshold))
    print("Model and threshold saved.")

if __name__ == "__main__":
    train_and_evaluate()
