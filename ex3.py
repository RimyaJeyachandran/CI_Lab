import csv
import math
import numpy as np
from collections import Counter
from sklearn.metrics import confusion_matrix, f1_score, recall_score, accuracy_score
from sklearn.model_selection import train_test_split

# --- DISTANCE UTILITIES ---
# Using NumPy makes these 10x faster and cleaner to read
def get_distance(p1, p2, metric='euclidean'):
    p1, p2 = np.array(p1), np.array(p2)
    if metric == 'euclidean':
        return np.sqrt(np.sum((p1 - p2)**2))
    elif metric == 'manhattan':
        return np.sum(np.abs(p1 - p2))
    elif metric == 'chebyshev':
        return np.max(np.abs(p1 - p2))
    return 0

# --- CORE LOGIC ---
def knn_predict(X_train, y_train, x_test, k, metric='euclidean', weighted=False):
    # Calculate all distances at once
    distances = [get_distance(x, x_test, metric) for x in X_train]
    
    # Get indices of the k smallest distances
    # Zip then sort is a very "human" way to keep labels attached to values
    neighbor_data = sorted(zip(distances, y_train), key=lambda x: x[0])[:k]

    if not weighted:
        # Just grab the most common label
        labels = [label for _, label in neighbor_data]
        return Counter(labels).most_common(1)[0][0]

    # Weighted logic: Closer neighbors get more "votes"
    class_weights = {}
    for dist, label in neighbor_data:
        # Handle zero-distance to avoid division by zero
        weight = 1 / (dist**2) if dist != 0 else 1e6
        class_weights[label] = class_weights.get(label, 0) + weight
    
    return max(class_weights, key=class_weights.get)

# --- DATA HANDLING ---
def load_dataset(path, attr_indices):
    """Loads CSV and extracts specific features and labels."""
    X, y = [], []
    try:
        with open(path, 'r') as f:
            reader = csv.reader(f)
            next(reader) # Skip header
            for row in reader:
                if not row: continue
                X.append([float(row[i]) for i in attr_indices])
                y.append(row[-1].strip())
    except FileNotFoundError:
        print(f"Error: Could not find file at {path}")
        return None, None
    
    return np.array(X), np.array(y)

# --- USER INTERFACE ---
def run_file_analysis():
    # Hardcoded paths in scripts are usually "placeholders" for humans
    data_path = r"C:\CI\iris.csv"
    
    indices_raw = input("Enter attribute indices (e.g., 0 1 2): ")
    indices = [int(i) for i in indices_raw.split()]

    X, y = load_dataset(data_path, indices)
    if X is None: return

    # Train/Test Split
    split_size = 1 - (int(input("Training % (e.g. 80): ")) / 100)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=split_size, random_state=42)

    # Heuristic for K
    k = int(len(X_train)**0.5) # A common "rule of thumb"
    if k % 2 == 0: k += 1
    print(f"Using calculated K: {k}")

    # Metrics selection map
    metrics = {1: 'euclidean', 2: 'manhattan', 3: 'chebyshev'}
    print("\n1: Euclidean | 2: Manhattan | 3: Chebyshev")
    m_choice = metrics.get(int(input("Choice: ")), 'euclidean')

    is_weighted = input("Use weighted KNN? (y/n): ").lower() == 'y'

    # Generate predictions
    print("Processing...")
    preds = [knn_predict(X_train, y_train, x, k, m_choice, is_weighted) for x in X_test]

    # Display Results
    print("\n" + "="*30)
    print(f"Accuracy:  {accuracy_score(y_test, preds):.2%}")
    print(f"F1-Score:  {f1_score(y_test, preds, average='weighted'):.2f}")
    print("\nConfusion Matrix:\n", confusion_matrix(y_test, preds))
    print("="*30)

if __name__ == "__main__":
    run_file_analysis()