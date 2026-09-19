import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import bisect

def V(x):
    return 0.0

def solve_se(E, N=10000, return_psi=False):
    dx = 1.0/N
    dx2 = dx**2
    x = 0
    psi = 0
    dpsi = 1
    x_vals = [0]
    psi_vals = [0]
    
    for i in range(N):
        d2psi = 2 * (V(x) - E) * psi
        d2psinew = 2 * (V(x + dx) - E) * (psi + dpsi * dx + 0.5 * d2psi * dx2)
        psi += dpsi * dx + 0.5 * d2psi * dx2
        dpsi += 0.5 * (d2psi + d2psinew) * dx
        x += dx
        if return_psi:
            x_vals.append(x)
            psi_vals.append(psi)
            
    if return_psi:
        return np.array(x_vals), np.array(psi_vals)
    return psi

# Finding roots of solve_se(E)
# Exact: pi^2 * n^2 / 2
eigenvalues = []
for n in range(1, 5):
    E_approx = (np.pi**2 * n**2 / 2)
    # Search in a range around E_approx
    E_min = E_approx * 0.9
    E_max = E_approx * 1.1
    # Check for sign change
    if solve_se(E_min) * solve_se(E_max) > 0:
        # Expand search range if necessary
        E_min = E_approx - 2.0
        E_max = E_approx + 2.0
        
    E_found = bisect(solve_se, E_min, E_max)
    eigenvalues.append(E_found)
    print(f"n={n}, E_exact={E_approx:.4f}, E_found={E_found:.4f}")

# Plotting eigenstates
plt.figure(figsize=(10,6))
for n, E in enumerate(eigenvalues, 1):
    x, psi = solve_se(E, return_psi=True)
    # Normalize for plotting
    psi = psi / np.max(np.abs(psi))
    plt.plot(x, psi, label=f"n={n}, E={E:.3f}")

plt.xlabel('x')
plt.ylabel('$\psi_n(x)$')
plt.title('Eigenstates for Infinite Box Potential')
plt.legend()
plt.grid(True)
plt.savefig('report/task2_eigenstates.png')
# plt.show()
