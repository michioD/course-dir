import numpy as np
import random
from scipy.optimize import minimize
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

# --- SVM Engine (Linear Kernel Implementation) ---

def kernel_linear(x: np.array,y: np.array):
    return np.dot(x, y)


def kernel_polynomial(x: np.array,y: np.array):
    p = 7
    return (np.dot(x,y)+1)**p

def kernel_radial(x, y, sigma=7.0):
    diff = np.subtract(x, y)
    return np.exp(-np.dot(diff, diff) / (2 * sigma ** 2))

kernel = kernel_linear
def solve_svm(x, t, kernel_func, C=1000):
    # [cite_start]"""Solves the dual optimization task[cite: 47]."""
    N = x.shape[0]
    # [cite_start]Pre-compute Matrix P [cite: 155]
    P = np.zeros((N, N))
    for i in range(N):
        for j in range(N):
            P[i, j] = t[i] * t[j] * kernel_func(x[i], x[j])

    def objective(alpha): 
        # [cite_start]Equation (4) [cite: 48]
        return 0.5 * np.dot(alpha, np.dot(P, alpha)) - np.sum(alpha)

    def zerofun(alpha): 
        # [cite_start]Equation (5) [cite: 54]
        return np.dot(alpha, t)

    # [cite_start]Bounds 0 <= alpha <= C [cite: 87]
    bounds = [(0, C) for _ in range(N)] 
    constraints = {'type': 'eq', 'fun': zerofun}
    
    # [cite_start]Minimize call [cite: 120]
    ret = minimize(objective, np.zeros(N), bounds=bounds, constraints=constraints)
    
    if not ret.success: 
        return None, None, False
    
    alpha = ret.x
    # [cite_start]
    sv_idx = [i for i in range(N) if alpha[i] > 1e-5] # Threshold for non-zero [cite: 174]
    
    if not sv_idx:
        return alpha, 0, True
    
    # [cite_start]Calculate threshold b [cite: 66]
    s = sv_idx[0]
    b = sum(alpha[i] * t[i] * kernel_func(x[s], x[i]) for i in range(N)) - t[s]
    return alpha, b, True

# --- Interactive Visualizer ---

class FullyFlexibleSVM:
    def __init__(self):
        # [cite_start]Initial Cluster Configuration [cite: 188]
        self.centers = {'A1': np.array([1.5, 0.5]), 'A2': np.array([-1.5, 0.5]), 'B': np.array([0.0, -1.0])}
        self.N_A = 10
        self.N_B = 20
        self.std_dev = 0.2
        self.C = 100.0 # Start with a moderate C
        self.selected_center = None
        
        self.fig, self.ax = plt.subplots(figsize=(9, 9))
        plt.subplots_adjust(bottom=0.30) # Make room for 3 sliders
        
        # --- Create Sliders ---
        # Axes positions: [left, bottom, width, height]
        ax_c = plt.axes([0.2, 0.15, 0.6, 0.03])
        ax_std = plt.axes([0.2, 0.10, 0.6, 0.03])
        ax_n = plt.axes([0.2, 0.05, 0.6, 0.03])
        
        # Slider Definitions
        # C ranges from 0.01 (very soft) to 1000 (very hard)
        self.slider_c = Slider(ax_c, 'Penalty (C)', 0.01, 100.0, valinit=self.C)
        self.slider_std = Slider(ax_std, 'Spread (Radius)', 0.05, 1.0, valinit=self.std_dev)
        self.slider_n = Slider(ax_n, 'Points (N)', 5, 50, valinit=self.N_A, valstep=1)
        
        # Connect updates
        self.slider_c.on_changed(self.update_params)
        self.slider_std.on_changed(self.update_params)
        self.slider_n.on_changed(self.update_params)
        
        # Connect mouse events
        self.fig.canvas.mpl_connect('button_press_event', self.on_click)
        self.fig.canvas.mpl_connect('button_release_event', self.on_release)
        self.fig.canvas.mpl_connect('motion_notify_event', self.on_motion)
        
        self.update_plot()
        plt.show()

    def update_params(self, val):
        self.C = self.slider_c.val
        self.std_dev = self.slider_std.val
        self.N_A = int(self.slider_n.val)
        self.N_B = self.N_A * 2
        self.update_plot()

    def get_data(self):
        """Generates random clusters."""
        np.random.seed(42) # Fixed seed for consistency while dragging
        a1 = np.random.randn(self.N_A, 2) * self.std_dev + self.centers['A1']
        a2 = np.random.randn(self.N_A, 2) * self.std_dev + self.centers['A2']
        b_pts = np.random.randn(self.N_B, 2) * self.std_dev + self.centers['B']
        
        x = np.concatenate((a1, a2, b_pts))
        t = np.concatenate((np.ones(self.N_A * 2), -np.ones(self.N_B)))
        return x, t, a1, a2, b_pts

    def update_plot(self):
        self.ax.clear()
        x_data, t_data, a1, a2, b_pts = self.get_data()
        
        # Pass the dynamic C value here
        alpha, b, success = solve_svm(x_data, t_data, kernel, self.C)
        
        # Plot clusters
        self.ax.scatter(a1[:,0], a1[:,1], c='blue', s=25, alpha=0.6, label='Class A')
        self.ax.scatter(a2[:,0], a2[:,1], c='blue', s=25, alpha=0.6)
        self.ax.scatter(b_pts[:,0], b_pts[:,1], c='red', s=25, alpha=0.6, label='Class B')
        
        if success and alpha is not None:
            xgrid = np.linspace(-4, 4, 50)
            ygrid = np.linspace(-4, 4, 50)
            X, Y = np.meshgrid(xgrid, ygrid)
            
            # Indicator functi
            def ind_func(p):
                # [cite_start]Eq (6) [cite: 59]
                return sum(alpha[i] * t_data[i] * kernel(p, x_data[i]) for i in range(len(alpha))) - b
            
            Z = np.array([[ind_func(np.array([px, py])) for px in xgrid] for py in ygrid])
            
            # Draw boundary and margins
            self.ax.contour(X, Y, Z, levels=[-1.0, 0.0, 1.0], 
                             colors=['red', 'black', 'blue'], 
                             linestyles=['dashed', 'solid', 'dashed'], 
                             linewidths=[1, 3, 1])
            
            self.ax.set_title(f"Linear SVM (C={self.C:.2f}, Radius={self.std_dev:.2f})")
            # self.ax.set_title(f" Polynomial SVM (C={self.C:.2f}, Radius={self.std_dev:.2f}), p = 10")
            # self.ax.set_title(f"RBF SVM (C={self.C:.2f}, Radius={self.std_dev:.2f}), sigma = 7")
        else:
            self.ax.text(0, 0, "OPTIMIZER FAILED\n(Try lowering C or Radius)", 
                         color='darkred', weight='bold', size=15, 
                         ha='center', va='center', bbox=dict(facecolor='white', alpha=0.8))
            self.ax.set_title(f"SVM: INFEASIBLE (C={self.C:.2f})")

        # Draw draggable handles
        for pos in self.centers.values():
            self.ax.plot(pos[0], pos[1], 'yo', markersize=12, markeredgecolor='k', alpha=0.8)
            
        self.ax.set_xlim(-4, 4)
        self.ax.set_ylim(-4, 4)
        self.ax.legend(loc='upper right')
        self.fig.canvas.draw_idle()

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
    FullyFlexibleSVM()
