# -*- coding: utf-8 -*-
# Python simulation of a partiocle in a 1d infinite box potential
# Integrate time independent SE using the Verlet method
# Boundary conditions are found by shooting
# MW 220513

from pylab import *
import numpy as np
import matplotlib.pyplot as plt
# parameters
N=100000              # number of mesh points
dx=5/N             # step length
dx2=dx**2          # step length squared

def delta_psi(E_input, even):
    E = E_input
    # potential energy function
    def V(x):
        y = x**2/2 + x**4/2
        #y = x**2/2 # harmonic oscillator
        #y = x**2/2 + x**4 # anharmonic oscillator
        return y

    # initial values and lists
    x = 0               # initial value of position x
    if even:
        psi = 1             # wave function at initial position
        dpsi = 0            # derivative of wave function at initial position
    else:
        psi = 0             # wave function at initial position
        dpsi = 1            # derivative of wave function at initial position
    x_tab = []          # list to store positions for plot
    psi_tab = []        # list to store wave function for plot
    x_tab.append(x)
    psi_tab.append(psi)
    for i in range(N) :
        d2psi = 2*(V(x)-E)*psi
        d2psinew = 2*(V(x+dx)-E)*psi
        psi += dpsi*dx + 0.5*d2psi*dx2
        dpsi += 0.5*(d2psi+d2psinew)*dx
        x += dx
        x_tab.append(x)
        psi_tab.append(psi)
    return x_tab,psi_tab

def find_eigenvalue(E_min, E_max, tol=1e-9, even=True):
    # Evaluate sign at E_min once before starting the loop
    _, psi_min = delta_psi(E_min, even)
    sign_min = np.sign(psi_min[-1])
    
    while (E_max - E_min) > tol:
        E_mid = (E_min + E_max) / 2
        _, psi_mid = delta_psi(E_mid, even)
        sign_mid = np.sign(psi_mid[-1])
        
        if sign_mid == sign_min:
            E_min = E_mid
        else:
            E_max = E_mid
            
    # Return the final refined energy and the corresponding wavefunction arrays
    E_target = (E_min + E_max) / 2
    x_tab, psi_tab = delta_psi(E_target, even)
    return E_target, x_tab, psi_tab

# 1. Set up the figure first before plotting anything
plt.figure(num=None, figsize=(8, 8), dpi=80, facecolor='w', edgecolor='k')

# 2. Run the binary search to bracket the ground state (E_1 = pi^2/2 ≈ 4.935)

# eigenvalue_4, x_tab_4, psi_tab_4 = find_eigenvalue(4.5, 5.5, even=True)
# 3. Plot the eigenstate

# 2. Run the binary search to bracket the anharmonic states
eigenvalue_0, x_tab_0, psi_tab_0 = find_eigenvalue(0.1, 1.5, even=True)
eigenvalue_1, x_tab_1, psi_tab_1 = find_eigenvalue(1.5, 3.0, even=False)
eigenvalue_2, x_tab_2, psi_tab_2 = find_eigenvalue(3.5, 5.0, even=True)
eigenvalue_3, x_tab_3, psi_tab_3 = find_eigenvalue(5.5, 8.0, even=False)
plt.plot(x_tab_0, psi_tab_0, linewidth=1, color='purple', label=f'Eigenstate 0 (E={eigenvalue_0:.3f})')
plt.plot(x_tab_1, psi_tab_1, linewidth=1, color='red', label=f'Eigenstate 1 (E={eigenvalue_1:.3f})')
plt.plot(x_tab_2, psi_tab_2, linewidth=1, color='blue', label=f'Eigenstate 2 (E={eigenvalue_2:.3f})')
plt.plot(x_tab_3, psi_tab_3, linewidth=1, color='green', label=f'Eigenstate 3 (E={eigenvalue_3:.3f})')
# plt.plot(x_tab_4, psi_tab_4, linewidth=1, color='orange', label=f'Eigenstate 4 (E={eigenvalue_4:.3f})')

plt.xlabel('x')
plt.ylabel('$\\psi$')
plt.legend()
# Limit the axes to hide the exponential blow-up at the tail
plt.xlim(0, 4.0)
plt.ylim(-1.5, 1.5)
plt.savefig('q4-eigenstate-plots.png')

# Theoretical Perturbation Calculations
print(f"{'n':<5} | {'Numerical E':<15} | {'Perturbation E':<15}")
print("-" * 40)
for n, num_E in enumerate([eigenvalue_0, eigenvalue_1, eigenvalue_2, eigenvalue_3]):
    # E_n = E_n^(0) + E_n^(1) = (n + 1/2) + 3/8 * (2*n**2 + 2*n + 1)
    pert_E = (n + 0.5) + (3/8) * (2*n**2 + 2*n + 1)
    print(f"{n:<5} | {num_E:<15.3f} | {pert_E:<15.3f}")

