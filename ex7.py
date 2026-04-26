import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_predict, StratifiedKFold
from sklearn.metrics import (accuracy_score, precision_score, 
                             recall_score, f1_score, confusion_matrix)
from tabulate import tabulate

def run_churn_analysis():
    # --- 1. User Configuration ---
    print("--- Churn Analysis Configuration ---")
    path = input("Enter dataset path: ").strip()
    trees = int(input("Number of trees (n_estimators): ") or 100)
    target = input("Name of target column: ").strip()
    folds = int(input("Number of CV folds: ") or 5)

    # --- 2. Data Loading & Cleaning ---
    try:
        # Using 'latin1' to handle special characters often found in CSVs
        df = pd.read_csv(path, encoding='latin1')
        print(f"\n[Success] Loaded {df.shape[0]} rows and {df.shape[1]} columns.")
    except Exception as e:
        print(f"[Error] Failed to load file: {e}")
        return

    # --- 3. Data Preparation ---
    # Separating features (X) and target (y)
    X = df.drop(columns=[target])
    y = df[target]

    # Convert text categories into dummy variables (One-Hot Encoding)
    X = pd.get_dummies(X)

    # --- 4. Feature Importance Diagnostic ---
    # Helping you find why accuracy is so high (Data Leakage check)
    diag_model = RandomForestClassifier(n_estimators=trees, random_state=42)
    diag_model.fit(X, y)
    
    importances = sorted(zip(X.columns, diag_model.feature_importances_), 
                         key=lambda x: x[1], reverse=True)
    
    print("\nTop Features (Check if any have suspiciously high importance):")
    print(tabulate(importances[:5], headers=["Feature", "Weight"], tablefmt="simple"))

    # --- 5. Model Evaluation (Cross-Validation) ---
    print(f"\nRunning {folds}-fold Cross-Validation...")
    clf = RandomForestClassifier(n_estimators=trees, random_state=42)
    cv_strategy = StratifiedKFold(n_splits=folds, shuffle=True, random_state=42)
    
    # Predict using cross-validation to get an honest assessment
    predictions = cross_val_predict(clf, X, y, cv=cv_strategy)

    # --- 6. Results & Metrics ---
    metrics = [
        ["Accuracy", accuracy_score(y, predictions)],
        ["Precision", precision_score(y, predictions, average='weighted', zero_division=0)],
        ["Recall", recall_score(y, predictions, average='weighted', zero_division=0)],
        ["F1 Score", f1_score(y, predictions, average='weighted', zero_division=0)]
    ]

    print("\n" + "="*25)
    print("   FINAL MODEL PERFORMANCE")
    print("="*25)
    print(tabulate(metrics, headers=["Metric", "Value"], tablefmt="grid", floatfmt=".4f"))

    # --- 7. Confusion Matrix ---
    labels = sorted(y.unique())
    cm = confusion_matrix(y, predictions)
    
    print("\nConfusion Matrix Visualization:")
    print(tabulate(
        cm,
        headers=[f"Pred: {l}" for l in labels],
        showindex=[f"Actual: {l}" for l in labels],
        tablefmt="grid"
    ))

if __name__ == "__main__":
    run_churn_analysis()