import numpy as np
import random, math
from scipy.optimize import minimize
import matplotlib.pyplot as plt

# --- 1. DATA GENERATION (As per Page 8) ---
np.random.seed(100) # Reproducibility

classA = np.concatenate(
    (np.random.randn(10, 2) * 0.2 + [1.5, 0.5],
     np.random.randn(10, 2) * 0.2 + [-1.5, 0.5]))
classB = np.random.randn(20, 2) * 0.2 + [0.0, -0.5]

inputs = np.concatenate((classA, classB))
targets = np.concatenate(
    (np.ones(classA.shape[0]),
     -np.ones(classB.shape[0])))

N = inputs.shape[0] # Number of rows (samples)

# Shuffle data (Important for optimization stability)
permute = list(range(N))
random.shuffle(permute)
x = inputs[permute, :]
t = targets[permute]

# --- 2. KERNEL FUNCTIONS ---
def kernel_linear(x, y):
    return np.dot(x, y)

def kernel_polynomial(x, y, p=2):
    return (np.dot(x, y) + 1) ** p

def kernel_radial(x, y, sigma=1.0):
    diff = np.subtract(x, y)
    return np.exp(-np.dot(diff, diff) / (2 * sigma ** 2))

# SELECT KERNEL HERE
# kernel_func = kernel_linear
# kernel_func = kernel_polynomial
kernel_func = kernel_radial 

# --- 3. PRE-COMPUTE MATRIX P ---
# P_ij = t_i * t_j * K(x_i, x_j)
P = np.zeros((N, N))
for i in range(N):
    for j in range(N):
        P[i][j] = t[i] * t[j] * kernel_func(x[i], x[j])

# --- 4. OPTIMIZATION ---
def objective(alpha):
    # Eq (4): 1/2 * alpha^T * P * alpha - sum(alpha)
    return 0.5 * np.dot(alpha, np.dot(P, alpha)) - np.sum(alpha)

def zerofun(alpha):
    # Eq (10): sum(alpha_i * t_i) = 0
    return np.dot(alpha, t)

C = 100 # Slack parameter
start = np.zeros(N) # Initial guess
B = [(0, C) for b in range(N)] # Bounds: 0 <= alpha <= C
XC = {'type':'eq', 'fun':zerofun} # Constraint

ret = minimize(objective, start, bounds=B, constraints=XC)

if not ret.success:
    print("WARNING: Optimizer failed to find a solution.")

alpha = ret.x

# --- 5. EXTRACT SUPPORT VECTORS & CALCULATE b ---
threshold = 1e-5
sv_indices = [i for i in range(N) if alpha[i] > threshold]

# Calculate b using Eq (7)
# It's better to average b over all Support Vectors for stability
b_sum = 0
for s_idx in sv_indices:
    # sum_i(alpha_i * t_i * K(x_s, x_i)) - t_s
    k_sum = 0
    for i in range(N):
        k_sum += alpha[i] * t[i] * kernel_func(x[s_idx], x[i])
    b_sum += (k_sum - t[s_idx])

if len(sv_indices) > 0:
    b = b_sum / len(sv_indices)
else:
    b = 0
    print("No Support Vectors found!")

# --- 6. INDICATOR FUNCTION ---
def indicator(s):
    # Eq (6): sum(alpha_i * t_i * K(s, x_i)) - b
    res = 0
    for i in range(N):
        # We only need to sum over non-zero alphas (Support Vectors)
        if alpha[i] > threshold:
            res += alpha[i] * t[i] * kernel_func(s, x[i])
    return res - b

# --- 7. PLOTTING ---
plt.figure(figsize=(8, 8))

# Plot data points
plt.plot([p[0] for p in classA], [p[1] for p in classA], 'b.', label='Class A (+)')
plt.plot([p[0] for p in classB], [p[1] for p in classB], 'r.', label='Class B (-)')

# Plot Support Vectors (circled)
for i in sv_indices:
    plt.plot(x[i][0], x[i][1], 'go', fillstyle='none', markersize=10)

# Generate Grid for Contour Plot
xgrid = np.linspace(-4, 4, 100)
ygrid = np.linspace(-4, 4, 100)
grid = np.zeros((len(xgrid), len(ygrid)))

for i, xi in enumerate(xgrid):
    for j, yi in enumerate(ygrid):
        # Pass the point as an array/vector to the indicator
        grid[j, i] = indicator(np.array([xi, yi])) # Note indices j, i for meshgrid orientation

# Contour plot
# Levels: -1 (margin), 0 (boundary), 1 (margin)
plt.contour(xgrid, ygrid, grid, (-1.0, 0.0, 1.0), 
            colors=('red', 'black', 'blue'), 
            linewidths=(1, 3, 1))

plt.title(f"SVM Decision Boundary ({kernel_func.__name__})")
plt.axis('equal')
plt.legend()
plt.show()
