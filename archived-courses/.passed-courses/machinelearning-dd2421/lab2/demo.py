import numpy as np
import random
from scipy.optimize import minimize
import matplotlib.pyplot as plt

# --- SVM Engine (Linear Kernel Implementation) ---



def kernel_linear(x: np.array,y: np.array):
    return np.dot(x, y)


def kernel_polynomial(x: np.array,y: np.array):
    p = 2
    return (np.dot(x,y)+1)**p

def kernel_radial(x, y, sigma=1.0):
    diff = np.subtract(x, y)
    return np.exp(-np.dot(diff, diff) / (2 * sigma ** 2))

kernel = kernel_radial
def solve_svm(x, t, C=1000):
    """
    Solves the dual optimization problem[cite: 47, 48]:
    Minimize 1/2 * sum(alpha_i * alpha_j * t_i * t_j * K(x_i, x_j)) - sum(alpha_i)
    Subject to: sum(alpha_i * t_i) = 0 and 0 <= alpha_i <= C[cite: 89, 87].
    """
    N = x.shape[0]
    # Pre-compute Matrix P: P_ij = t_i * t_j * K(x_i, x_j) [cite: 155]
    P = np.zeros((N, N))
    for i in range(N):
        for j in range(N):
            P[i, j] = t[i] * t[j] * kernel(x[i], x[j])

    def objective(alpha):
        return 0.5 * np.dot(alpha, np.dot(P, alpha)) - np.sum(alpha)

    def zerofun(alpha):
        return np.dot(alpha, t)

    # Constraints: equality to zero and bounds [cite: 122, 142]
    bounds = [(0, C) for _ in range(N)]
    constraints = {'type': 'eq', 'fun': zerofun}
    
    ret = minimize(objective, np.zeros(N), bounds=bounds, constraints=constraints)
    
    # Check if the optimizer found a solution [cite: 170]
    if not ret.success:
        return None, None, False
    
    alpha = ret.x
    # Identify support vectors (alpha > 0) [cite: 63, 174]
    sv_idx = [i for i in range(N) if alpha[i] > 1e-5]
    if not sv_idx:
        return alpha, 0, True
    
    # Calculate b from a support vector [cite: 66]
    s = sv_idx[0]
    b = sum(alpha[i] * t[i] * kernel(x[s], x[i]) for i in range(N)) - t[s]
    return alpha, b, True

# --- Interactive Visualizer ---

class InteractiveLinearSVM:
    def __init__(self):
        # Center points for clusters [cite: 188, 190]
        self.centers = {
            'A1': np.array([1.5, 0.5]),
            'A2': np.array([-1.5, 0.5]),
            'B': np.array([0.0, -1.0])
        }
        self.selected_center = None
        self.C = 1000  # High C acts like a hard-margin; fails if overlapping
        
        self.fig, self.ax = plt.subplots(figsize=(8, 7))
        self.fig.canvas.mpl_connect('button_press_event', self.on_click)
        self.fig.canvas.mpl_connect('button_release_event', self.on_release)
        self.fig.canvas.mpl_connect('motion_notify_event', self.on_motion)
        
        self.update_plot()
        plt.show()

    def get_data(self):
        """Generates clusters around centers with standard deviation 0.2[cite: 191]."""
        np.random.seed(42)
        std = 0.2
        a1 = np.random.randn(10, 2) * std + self.centers['A1']
        a2 = np.random.randn(10, 2) * std + self.centers['A2']
        b_pts = np.random.randn(20, 2) * std + self.centers['B']
        
        x = np.concatenate((a1, a2, b_pts))
        t = np.concatenate((np.ones(20), -np.ones(20)))
        return x, t, a1, a2, b_pts

    def update_plot(self):
        self.ax.clear()
        x_data, t_data, a1, a2, b_pts = self.get_data()
        
        # Solve SVM
        alpha, b, success = solve_svm(x_data, t_data, self.C)
        
        # Plot data clusters [cite: 214, 215]
        self.ax.scatter(a1[:,0], a1[:,1], c='blue', s=20, alpha=0.5, label='Class A (+1)')
        self.ax.scatter(a2[:,0], a2[:,1], c='blue', s=20, alpha=0.5)
        self.ax.scatter(b_pts[:,0], b_pts[:,1], c='red', s=20, alpha=0.5, label='Class B (-1)')
        
        if success and alpha is not None:
            # Generate grid to draw decision boundary [cite: 231]
            x_min, x_max = -4, 4
            y_min, y_max = -4, 4
            xgrid = np.linspace(x_min, x_max, 50)
            ygrid = np.linspace(y_min, y_max, 50)
            X, Y = np.meshgrid(xgrid, ygrid)
            
            # Indicator function: sum(alpha_i * t_i * K(s, x_i)) - b [cite: 59]
            def ind_func(p):
                return sum(alpha[i] * t_data[i] * kernel(p, x_data[i]) for i in range(len(alpha))) - b
            
            Z = np.array([[ind_func(np.array([px, py])) for px in xgrid] for py in ygrid])
            
            # Draw boundary (0) and margins (-1, 1) [cite: 230]
            self.ax.contour(X, Y, Z, levels=[-1.0, 0.0, 1.0], 
                             colors=['red', 'black', 'blue'], 
                             linestyles=['dashed', 'solid', 'dashed'],
                             linewidths=[1, 3, 1])
            self.ax.set_title("Linear SVM: Drag the yellow centers")
        else:
            # Visual indication of optimizer failure [cite: 243]
            self.ax.text(0, 0, "OPTIMIZER FAILED\n(Data not linearly separable)", 
                         color='darkred', weight='bold', size=15, 
                         ha='center', va='center', bbox=dict(facecolor='white', alpha=0.8))
            self.ax.set_title("Linear SVM: INFEASIBLE SOLUTION", color='red')

        # Draw interactive center handles
        for name, pos in self.centers.items():
            self.ax.plot(pos[0], pos[1], 'yo', markersize=12, markeredgecolor='k')
            
        self.ax.set_xlim(-4, 4)
        self.ax.set_ylim(-4, 4)
        self.ax.legend(loc='upper right')
        self.fig.canvas.draw()

    def on_click(self, event):
        if event.inaxes != self.ax: return
        for name, pos in self.centers.items():
            if np.linalg.norm(np.array([event.xdata, event.ydata]) - pos) < 0.4:
                self.selected_center = name
                break

    def on_release(self, event):
        self.selected_center = None

    def on_motion(self, event):
        if self.selected_center and event.inaxes == self.ax:
            self.centers[self.selected_center] = np.array([event.xdata, event.ydata])
            self.update_plot()

if __name__ == "__main__":
    InteractiveLinearSVM()
