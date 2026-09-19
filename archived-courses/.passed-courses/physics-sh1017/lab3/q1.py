# -*- coding: utf-8 -*-
# Python simulation of a partiocle in a 1d infinite box potential
# Integrate time independent SE using the Verlet method
# Boundary conditions are found by shooting
# MW 220513

from pylab import *
import numpy as np
import matplotlib.pyplot as plt

# trial energy
E=0.5*np.pi**2


# potential energy function
def V(x):
    y = 0.0
    #y = x**2/2 # harmonic oscillator
    #y = x**2/2 + x**4 # anharmonic oscillator
    return y

def delta_psi(N):
    dx=1/N             # step length
    dx2=dx**2          # step length squared

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
    return abs(psi)


psis = [delta_psi(N) for N in [10, 100, 1000, 10000, 100000]]

plt.loglog([10, 100, 1000, 10000, 100000], np.abs(psis), marker='o', label='(Numerically integrated)$\Delta$')
# plot the log log but add grid lines to the plot
plt.grid(True, which="both", ls="-", alpha=0.2)
plt.xlabel('N (number of mesh points)')
plt.ylabel('$\Delta =|\psi(1)|$')
plt.loglog([10, 100, 1000, 10000, 100000], [1/N**2 for N in [10, 100, 1000, 10000, 100000]], 'r--', label='(Theoretical)$\Delta = constant/N^2$')
plt.legend()
plt.savefig('q1-delta_psi.png')