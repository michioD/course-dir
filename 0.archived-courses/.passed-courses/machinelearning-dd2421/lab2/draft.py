import numpy as np
import random, math
from scipy.optimize import minimize
import matplotlib.pyplot as plt
from test_data import classA, classB



# x training data
x = np.concatenate((classA,classB))

t = np.concatenate(
        (np.ones(classA.shape[0]),
         -np.ones(classB.shape[0])))
C = 100
N = x.shape[0]
B = [(0,C) for b in range(N)]
alpha0 = np.ones(N)
permute = list(range(N))
np.random.shuffle(permute)
x = x[permute, :]
t = targets[permute]




def kernel_linear(x: np.array,y: np.array):
    return np.dot(x, y)


def kernel_polynomial(x: np.array,y: np.array):
    p = 2
    return (np.dot(x,y)+1)**p

def kernel_radial(x, y, sigma=1.0):
    diff = np.subtract(x, y)
    return np.exp(-np.dot(diff, diff) / (2 * sigma ** 2))


kernel = kernel_radial


p = np.zeros((N,N))
for i in range(N):
    for j in range(N):
        p[i][j] = t[i] * t[j] * kernel(x[i],x[j])

def objective(alpha):

    return 0.5 * np.dot(alpha, np.dot(p,alpha)) - np.sum(alpha) 


def zerofun(alpha):
    return np.dot(alpha,t)

constraint = {'type':'eq', 'fun': zerofun}





ret = minimize(objective, alpha0, bounds = B, constraints = constraint)

alpha = ret.x

def get_non_zero(alpha: np.array):
    tau = 1E-5
    n = len(alpha)
    non_zero_idx = []
    for i in range(n):
        if np.abs(alpha[i]) > tau:
            non_zero_idx.append(i)
    return non_zero_idx

def get_b(alpha):
    k = get_non_zero(alpha)[1]
    result = -t[k]
    for i in range(N):
        result += alpha[i] * t[i] * kernel(x[k], x[i])

    return result


def indicator(s):
    result = -b
    n = len(s)
    for i in range(n):
        result += alpha[i] * t[i] * kernel(s,x[i]) 
    return np.sign(result)

# b = get_b(alpha)
# sv_indices = get_non_zero(alpha)

# # 1. Define the grid resolution
# grid_size = 100
# x_min, x_max = x[:, 0].min() - 1, x[:, 0].max() + 1
# y_min, y_max = x[:, 1].min() - 1, x[:, 1].max() + 1
#
# x_range = np.linspace(x_min, x_max, grid_size)
# y_range = np.linspace(y_min, y_max, grid_size)
# grid_x, grid_y = np.meshgrid(x_range, y_range)
#
# # 2. Compute the decision values for the entire grid
# # We flatten the grid to pass points through the indicator function
# grid_points = np.c_[grid_x.ravel(), grid_y.ravel()]
# z_values = np.array([indicator(p) for p in grid_points])
# z_values = z_values.reshape(grid_x.shape)
#
# # 3. Plotting
# plt.figure(figsize=(8, 8))
#
# # Plot the data points
# plt.scatter(classA[:, 0], classA[:, 1], color='red', label='Class A')
# plt.scatter(classB[:, 0], classB[:, 1], color='blue', label='Class B')
#
# # Draw the boundary (level 0) and the margins (levels -1 and 1)
# plt.contour(grid_x, grid_y, z_values, 
#             levels=[-1.0, 0.0, 1.0], 
#             colors=('blue', 'black', 'red'), 
#             linestyles=('--', '-', '--'), 
#             linewidths=(1, 2, 1))
#
# plt.title(f"Non-Linear Boundary ({kernel.__name__})")
# plt.legend()
# plt.show()
