import math
import pandas as pd
import numpy as np
from collections import Counter
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, classification_report

# --- MATH CORE ---

def get_entropy(labels):
    counts = np.bincount(labels) if isinstance(labels[0], int) else Counter(labels).values()
    probs = [count / len(labels) for count in counts]
    return -sum(p * math.log2(p) for p in probs if p > 0)

def get_gini(labels):
    counts = Counter(labels).values()
    return 1 - sum((count / len(labels))**2 for count in counts)

# --- TREE LOGIC ---

def calculate_gain(df, attribute, target, metric_func):
    """Calculates how much 'cleaner' the data gets by splitting on an attribute."""
    parent_impurity = metric_func(df[target])
    
    # Calculate weighted average of impurity after split
    values = df[attribute].unique()
    weighted_impurity = 0
    
    for val in values:
        subset = df[df[attribute] == val][target]
        weighted_impurity += (len(subset) / len(df)) * metric_func(subset)
        
    return parent_impurity - weighted_impurity

def build_tree(df, attributes, target, metric_func):
    """Recursive function to grow the tree."""
    target_values = df[target]

    # Base Case 1: Pure leaf (all items have same label)
    if len(target_values.unique()) == 1:
        return target_values.iloc[0]

    # Base Case 2: No more attributes to split on
    if not attributes:
        return target_values.mode()[0]

    # Find the best split
    gains = {attr: calculate_gain(df, attr, target, metric_func) for attr in attributes}
    best_attr = max(gains, key=gains.get)
    
    # Recursively build branches
    tree = {best_attr: {}}
    remaining_attrs = [a for a in attributes if a != best_attr]

    for val in df[best_attr].unique():
        subset = df[df[best_attr] == val]
        tree[best_attr][val] = build_tree(subset, remaining_attrs, target, metric_func)

    return tree

# --- INTERFACE & MODES ---

def run_manual_mode(metric_func):
    cols = input("Enter column names (comma separated, target last): ").split(",")
    cols = [c.strip() for c in cols]
    
    print(f"Enter data rows (comma separated). Type 'done' to finish.")
    rows = []
    while True:
        line = input("> ")
        if line.lower() == 'done': break
        rows.append(line.split(","))
    
    df = pd.DataFrame(rows, columns=cols)
    target = cols[-1]
    features = cols[:-1]

    print("\nBuilding Decision Tree...")
    tree = build_tree(df, features, target, metric_func)
    print("\nFinal Tree Structure:", tree)

def run_csv_mode(criterion):
    path = input("Path to CSV: ")
    target = input("Target column: ")
    
    df = pd.read_csv(path)
    
    # Label Encoding (human developers usually do this in one line)
    le = LabelEncoder()
    for col in df.select_dtypes(include=['object']).columns:
        df[col] = le.fit_transform(df[col])

    X = df.drop(columns=[target])
    y = df[target]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = DecisionTreeClassifier(criterion=criterion)
    model.fit(X_train, y_train)
    
    preds = model.predict(X_test)
    print("\n--- Model Report ---")
    print(f"Accuracy: {accuracy_score(y_test, preds):.2%}")
    print(classification_report(y_test, preds))

def main():
    menu = {
        '1': ("Manual Input", run_manual_mode),
        '2': ("CSV Import", run_csv_mode),
        '3': ("Exit", exit)
    }

    while True:
        print("\n--- DECISION TREE TOOL ---")
        for k, v in menu.items(): print(f"{k}. {v[0]}")
        
        choice = input("Select: ")
        if choice not in menu: continue
        if choice == '3': break

        crit_choice = input("Splitting Criterion (1: Entropy, 2: Gini): ")
        metric = get_entropy if crit_choice == '1' else get_gini
        crit_str = "entropy" if crit_choice == '1' else "gini"

        # Execute chosen function
        if choice == '1': menu[choice][1](metric)
        else: menu[choice][1](crit_str)

if __name__ == "__main__":
    main()