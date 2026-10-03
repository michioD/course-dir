import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import bisect

def V(x):
    return 0.5 * x**2

def solve_se_ho(E, parity, N=10000, return_psi=False):
    # parity: 0 for even, 1 for odd
    xmax = 5.0
    dx = xmax/N
    dx2 = dx**2
    x = 0
    if parity == 0: # even
        psi = 1.0
        dpsi = 0.0
    else: # odd
        psi = 0.0
        dpsi = 1.0
        
    x_vals = [0]
    psi_vals = [psi]
    
    for i in range(N):
        d2psi = 2 * (V(x) - E) * psi
        # Prediction of psi at x+dx
        psi_next = psi + dpsi * dx + 0.5 * d2psi * dx2
        d2psinew = 2 * (V(x + dx) - E) * psi_next
        psi = psi_next
        dpsi += 0.5 * (d2psi + d2psinew) * dx
        x += dx
        if return_psi:
            x_vals.append(x)
            psi_vals.append(psi)
            
    if return_psi:
        return np.array(x_vals), np.array(psi_vals)
    return psi

# Eigenvalues for HO
eigenvalues = []
for n in range(4):
    E_approx = n + 0.5
    parity = n % 2
    # Search range
    E_min = E_approx - 0.2
    E_max = E_approx + 0.2
    
    # Check for sign change
    if solve_se_ho(E_min, parity) * solve_se_ho(E_max, parity) > 0:
        # Broaden search
        E_min = E_approx - 0.5
        E_max = E_approx + 0.5
        
    E_found = bisect(lambda E: solve_se_ho(E, parity), E_min, E_max)
    eigenvalues.append(E_found)
    print(f"n={n}, E_exact={E_approx:.4f}, E_found={E_found:.4f}")

# Plotting eigenstates
plt.figure(figsize=(10,6))
for n, E in enumerate(eigenvalues):
    parity = n % 2
    x, psi = solve_se_ho(E, parity, return_psi=True)
    # Normalize for plotting
    psi = psi / np.max(np.abs(psi))
    plt.plot(x, psi, label=f"n={n}, E={E:.3f}")

plt.xlabel('x')
plt.ylabel('$\psi_n(x)$')
plt.title('Eigenstates for Harmonic Oscillator')
plt.legend()
plt.grid(True)
plt.savefig('report/task3_eigenstates.png')
# plt.show()
