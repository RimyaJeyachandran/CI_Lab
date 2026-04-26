import numpy as np
from tabulate import tabulate

def get_activation(net, method):
    if method == 'threshold':
        return 1 if net >= 1 else 0
    elif method == 'threshold_bipolar':
        return 1 if net >= 1 else -1
    elif method == 'sigmoid':
        return 1 / (1 + np.exp(-net))
    elif method == 'tanh':
        return np.tanh(net)
    return net

def get_derivative(out, method):
    if method == 'sigmoid':
        return out * (1 - out)
    elif method == 'tanh':
        return 1 - out**2
    return 1 # Default for threshold functions

# --- Getting User Inputs ---
print("--- Perceptron Configuration ---")
n_rows = int(input("Number of samples: "))
n_cols = int(input("Number of features: "))

X = []
for i in range(n_rows):
    row = input(f"Enter values for Sample {i+1} (space separated): ").split()
    X.append([float(val) for val in row])
X = np.array(X)

y = []
for i in range(n_rows):
    y.append(float(input(f"Target for Sample {i+1}: ")))

print("\n--- Initial Parameters ---")
w = np.array([float(val) for val in input(f"Enter {n_cols} initial weights: ").split()])
b = float(input("Enter initial bias: "))
lr = float(input("Learning rate: "))
epochs = int(input("Max epochs: "))

# Auto-detect if we are working with binary (0,1) or bipolar (-1, 1)
is_bipolar = -1 in X or -1 in y
print(f"\nSystem detected: {'Bipolar' if is_bipolar else 'Binary'} data.")
act_fn = input("Choose activation (threshold, threshold_bipolar, sigmoid, tanh): ").lower()

# --- Training Process ---
for ep in range(1, epochs + 1):
    epoch_results = []
    converged = True

    for i in range(n_rows):
        # Forward Pass
        net = np.dot(X[i], w) + b
        out = get_activation(net, act_fn)
        
        # Calculate Error and Gradient
        error = y[i] - out
        grad = get_derivative(out, act_fn)
        
        # Calculate Adjustments
        dw = lr * error * grad * X[i]
        db = lr * error * grad
        
        # Check if we are still learning
        if np.any(np.abs(dw) > 1e-6) or abs(db) > 1e-6:
            converged = False
        
        # Apply updates
        w += dw
        b += db
        
        # Log for display
        epoch_results.append([
            X[i], y[i], round(net, 3), round(out, 3), 
            np.round(dw, 3), round(db, 3), np.round(w.copy(), 3), round(b, 3)
        ])

    print(f"\n[Epoch {ep}]")
    headers = ["X", "Targ", "Net", "Out", "dw", "db", "New W", "New B"]
    print(tabulate(epoch_results, headers=headers, tablefmt="simple"))

    if converged:
        print(f"\nDone! Training converged at epoch {ep}.")
        break
else:
    print("\nStopped: Reached max epochs without full convergence.")

print("-" * 30)
print(f"Final Weights: {w}")
print(f"Final Bias:    {b}")