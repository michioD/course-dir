import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import bisect

def V(x):
    return 0.5 * x**2 + 0.5 * x**4

def solve_se_anharmonic(E, parity, N=10000, return_psi=False):
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
        psi_next = psi + dpsi * dx + 0.5 * d2psi * dx2
        d2psinew = 2 * (V(x + dx) - E) * psi_next
        psi = psi_next
        dpsi += 0.5 * (d2psi + d2psinew) * dx
        x += dx
        if return_psi:
            x_vals.append(x)
            psi_vals.append(psi)
        # Prevent overflow
        if abs(psi) > 1e10:
            break
            
    if return_psi:
        return np.array(x_vals), np.array(psi_vals)
    return psi

# Finding first 4 eigenvalues for anharmonic potential
# We can scan for sign changes first
eigenvalues = []
E_vals = np.linspace(0, 20, 200)

for parity in [0, 1]:
    results = []
    for E in E_vals:
        results.append(solve_se_anharmonic(E, parity))
    
    results = np.array(results)
    # Find sign changes
    sign_changes = np.where(np.diff(np.sign(results)))[0]
    for idx in sign_changes:
        E_min = E_vals[idx]
        E_max = E_vals[idx+1]
        try:
            E_found = bisect(lambda E: solve_se_anharmonic(E, parity), E_min, E_max)
            eigenvalues.append((E_found, parity))
        except ValueError:
            pass

# Sort eigenvalues by energy
eigenvalues.sort()

# Keep first 4
eigenvalues = eigenvalues[:4]

for i, (E, parity) in enumerate(eigenvalues):
    print(f"n={i}, E_found={E:.4f}, parity={'even' if parity==0 else 'odd'}")

# Plotting
plt.figure(figsize=(10,6))
for i, (E, parity) in enumerate(eigenvalues):
    x, psi = solve_se_anharmonic(E, parity, return_psi=True)
    psi = psi / np.max(np.abs(psi))
    plt.plot(x, psi, label=f"n={i}, E={E:.3f}")

plt.xlabel('x')
plt.ylabel('$\psi_n(x)$')
plt.title('Eigenstates for Anharmonic Oscillator $V(x)=x^2/2 + x^4/2$')
plt.legend()
plt.grid(True)
plt.savefig('report/task4_eigenstates.png')
# plt.show()
