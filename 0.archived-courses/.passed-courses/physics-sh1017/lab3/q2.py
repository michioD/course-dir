# -*- coding: utf-8 -*-
# Python simulation of a partiocle in a 1d infinite box potential
# Integrate time independent SE using the Verlet method
# Boundary conditions are found by shooting
# MW 220513

from pylab import *
import numpy as np
import matplotlib.pyplot as plt
# parameters
N=10000               # number of mesh points
dx=1/N             # step length
dx2=dx**2          # step length squared

def delta_psi(E_input):
    E = E_input

    # potential energy function
    def V(x):
        y = 0.0
        #y = x**2/2 # harmonic oscillator
        #y = x**2/2 + x**4 # anharmonic oscillator
        return y

    # initial values and lists
    x = 0               # initial value of position x
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

def find_eigenvalue(E_min, E_max, tol=1e-9):
    # Evaluate sign at E_min once before starting the loop
    _, psi_min = delta_psi(E_min)
    sign_min = np.sign(psi_min[-1])
    
    while (E_max - E_min) > tol:
        E_mid = (E_min + E_max) / 2
        _, psi_mid = delta_psi(E_mid)
        sign_mid = np.sign(psi_mid[-1])
        
        if sign_mid == sign_min:
            E_min = E_mid
        else:
            E_max = E_mid
            
    # Return the final refined energy and the corresponding wavefunction arrays
    E_target = (E_min + E_max) / 2
    x_tab, psi_tab = delta_psi(E_target)
    return E_target, x_tab, psi_tab

# 1. Set up the figure first before plotting anything
plt.figure(num=None, figsize=(8, 8), dpi=80, facecolor='w', edgecolor='k')

# 2. Run the binary search to bracket the ground state (E_1 = pi^2/2 ≈ 4.935)
eigenvalue_1, x_tab_1, psi_tab_1 = find_eigenvalue(0.4 * np.pi**2, 0.6 * np.pi**2)
eigenvalue_2, x_tab_2, psi_tab_2 = find_eigenvalue(1 * np.pi**2, 3 * np.pi**2)
eigenvalue_3, x_tab_3, psi_tab_3 = find_eigenvalue(3 * np.pi**2, 5 * np.pi**2)
eigenvalue_4, x_tab_4, psi_tab_4 = find_eigenvalue(7 * np.pi**2, 9 * np.pi**2)
# 3. Plot the eigenstate
plt.plot(x_tab_1, psi_tab_1, linewidth=1, color='red', label=f'Eigenstate 1 (E={eigenvalue_1:.3f})')
plt.plot(x_tab_2, psi_tab_2, linewidth=1, color='blue', label=f'Eigenstate 2 (E={eigenvalue_2:.3f})')
plt.plot(x_tab_3, psi_tab_3, linewidth=1, color='green', label=f'Eigenstate 3 (E={eigenvalue_3:.3f})')
plt.plot(x_tab_4, psi_tab_4, linewidth=1, color='orange', label=f'Eigenstate 4 (E={eigenvalue_4:.3f})')

plt.xlabel('x')
plt.ylabel('$\\psi$')
plt.legend()
plt.savefig('q2-eigenstate-plots.png')
print(f"E1 = {eigenvalue_1:.3f}")
print(f"E2 = {eigenvalue_2:.3f}")
print(f"E3 = {eigenvalue_3:.3f}")
print(f"E4 = {eigenvalue_4:.3f}")
