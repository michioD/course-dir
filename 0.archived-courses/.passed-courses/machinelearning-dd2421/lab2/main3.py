import numpy as np
import random
from scipy.optimize import minimize
import matplotlib.pyplot as plt

# --- SVM ENGINE (From Lab Instructions) ---

def kernel_radial(x, y, sigma=1.0):
    return np.exp(-np.linalg.norm(x-y)**2 / (2 * (sigma**2)))

def solve_svm(x, t, kernel_func, C=10):
    N = x.shape[0]
    # Pre-compute Matrix P [cite: 154, 155]
    P = np.zeros((N, N))
    for i in range(N):
        for j in range(N):
            P[i, j] = t[i] * t[j] * kernel_func(x[i], x[j])

    def objective(alpha): # [cite: 124]
        return 0.5 * np.dot(alpha, np.dot(P, alpha)) - np.sum(alpha)

    def zerofun(alpha): # [cite: 162]
        return np.dot(alpha, t)

    B = [(0, C) for _ in range(N)] # [cite: 128]
    XC = {'type': 'eq', 'fun': zerofun}
    
    ret = minimize(objective, np.zeros(N), bounds=B, constraints=XC)
    if not ret.success: return None, None
    
    alpha = ret.x
    sv_idx = [i for i in range(N) if alpha[i] > 1e-5]
    if not sv_idx: return alpha, 0
    
    # Calculate b [cite: 66]
    s = sv_idx[0]
    b = sum(alpha[i] * t[i] * kernel_func(x[s], x[i]) for i in range(N)) - t[s]
    return alpha, b

# --- INTERACTIVE CLASS ---

class InteractiveSVM:
    def __init__(self):
        # Initial Cluster Centers [cite: 190, 196, 197]
        self.centers = {
            'A1': np.array([1.5, 0.5]),
            'A2': np.array([-1.5, 0.5]),
            'B': np.array([0.0, -0.5])
        }
        self.selected_center = None
        self.fig, self.ax = plt.subplots(figsize=(8, 7))
        self.sigma = 1.0
        self.C = 10.0
        
        self.fig.canvas.mpl_connect('button_press_event', self.on_click)
        self.fig.canvas.mpl_connect('button_release_event', self.on_release)
        self.fig.canvas.mpl_connect('motion_notify_event', self.on_motion)
        
        self.update_plot()
        plt.show()

    def get_data(self):
        # Generate points around centers [cite: 196, 197]
        np.random.seed(42) # Keep noise consistent while dragging
        a1 = np.random.randn(10, 2) * 0.2 + self.centers['A1']
        a2 = np.random.randn(10, 2) * 0.2 + self.centers['A2']
        b_pts = np.random.randn(20, 2) * 0.2 + self.centers['B']
        
        x = np.concatenate((a1, a2, b_pts))
        t = np.concatenate((np.ones(20), -np.ones(20)))
        return x, t, a1, a2, b_pts

    def update_plot(self):
        self.ax.clear()
        x_data, t_data, a1, a2, b_pts = self.get_data()
        
        # Solve SVM
        alpha, b = solve_svm(x_data, t_data, kernel_radial, self.C)
        
        # Plot Clusters
        self.ax.scatter(a1[:,0], a1[:,1], c='blue', s=20, alpha=0.5, label='Class A')
        self.ax.scatter(a2[:,0], a2[:,1], c='blue', s=20, alpha=0.5)
        self.ax.scatter(b_pts[:,0], b_pts[:,1], c='red', s=20, alpha=0.5, label='Class B')
        
        # Plot Boundary [cite: 230]
        if alpha is not None:
            xgrid = np.linspace(-4, 4, 40)
            ygrid = np.linspace(-4, 4, 40)
            X, Y = np.meshgrid(xgrid, ygrid)
            
            def ind(p):
                return sum(alpha[i] * t_data[i] * kernel_radial(p, x_data[i], self.sigma) for i in range(len(alpha))) - b
            
            Z = np.array([[ind(np.array([px, py])) for px in xgrid] for py in ygrid])
            self.ax.contour(X, Y, Z, levels=[-1.0, 0.0, 1.0], colors=['red', 'black', 'blue'], linewidths=[1, 2, 1])

        # Draw draggable handles (centers)
        for name, pos in self.centers.items():
            self.ax.plot(pos[0], pos[1], 'ko', markersize=10, mfc='yellow', label=f'Center {name}')
            
        self.ax.set_title("Drag the yellow centers! (SVM Radial Kernel)")
        self.ax.set_xlim(-4, 4); self.ax.set_ylim(-4, 4)
        self.fig.canvas.draw()

    def on_click(self, event):
        if event.inaxes != self.ax: return
        for name, pos in self.centers.items():
            if np.linalg.norm(np.array([event.xdata, event.ydata]) - pos) < 0.3:
                self.selected_center = name
                break

    def on_release(self, event):
        self.selected_center = None

    def on_motion(self, event):
        if self.selected_center and event.inaxes == self.ax:
            self.centers[self.selected_center] = np.array([event.xdata, event.ydata])
            self.update_plot()

InteractiveSVM()
