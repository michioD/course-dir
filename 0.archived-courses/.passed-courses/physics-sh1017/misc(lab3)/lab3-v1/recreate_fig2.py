import numpy as np
import matplotlib.pyplot as plt

def solve_shooting_box(E, N=10000):
    dx = 1.0 / N
    dx2 = dx**2
    x = 0.0
    psi = 0.0
    dpsi = 1.0 # Initial slope
    
    x_tab = np.zeros(N+1)
    psi_tab = np.zeros(N+1)
    
    for i in range(N):
        x_tab[i] = x
        psi_tab[i] = psi
        
        # Verlet-like integration as used in the lab code
        d2psi = -2 * E * psi
        psi_next = psi + dpsi*dx + 0.5*d2psi*dx2
        d2psi_next = -2 * E * psi_next
        dpsi += 0.5*(d2psi + d2psi_next)*dx
        
        psi = psi_next
        x += dx
        
    x_tab[N] = x
    psi_tab[N] = psi
    return psi_tab, x_tab

def find_eigenvalue(E_min, E_max, tol=1e-10):
    # Binary search for E where psi(1) == 0
    while (E_max - E_min) > tol:
        E_mid = (E_min + E_max) / 2
        psi_mid = solve_shooting_box(E_mid)[0][-1]
        psi_min = solve_shooting_box(E_min)[0][-1]
        
        if np.sign(psi_mid) == np.sign(psi_min):
            E_min = E_mid
        else:
            E_max = E_mid
    return (E_min + E_max) / 2

# Find the first 4 eigenvalues
# Intervals chosen to contain pi^2*n^2/2: ~4.9, ~19.7, ~44.4, ~79.0
search_intervals = [(1, 10), (10, 30), (30, 60), (60, 100)]
eigenvalues = [find_eigenvalue(low, high) for low, high in search_intervals]

plt.figure(figsize=(10, 7))

colors = ['tab:blue', 'tab:orange', 'tab:green', 'tab:red']
for i, E in enumerate(eigenvalues):
    n = i + 1
    psi_vals, x_vals = solve_shooting_box(E)
    
    # Scale for visualization similar to the report (max amplitude ~0.3-0.4)
    # The report uses unnormalized but scaled output
    psi_plot = psi_vals / (np.max(np.abs(psi_vals)) * 2.5)
    
    plt.plot(x_vals, psi_plot, label=f'n={n}, E$_n$={E:.2f}', color=colors[i])

# Replicate the styling from the example report
plt.title('Eigenstates for n=1,2,3,4 and their corresponding eigenvalue energies')
plt.xlabel('x')
plt.ylabel('$\psi$')
plt.axhline(0, color='yellow', linewidth=1) # The report has a yellow-ish horizontal axis line
plt.axvline(0, color='yellow', linestyle=':', linewidth=1)
plt.axvline(1, color='yellow', linestyle=':', linewidth=1)
plt.grid(True, which='both', linestyle='-', alpha=0.3)
plt.legend()
plt.xlim(-0.05, 1.05)
plt.ylim(-0.45, 0.45)

plt.savefig('report/replicated_fig2.png')
print("Replicated Figure 2 saved to report/replicated_fig2.png")
for i, E in enumerate(eigenvalues):
    print(f"n={i+1}: E={E:.3f}")
