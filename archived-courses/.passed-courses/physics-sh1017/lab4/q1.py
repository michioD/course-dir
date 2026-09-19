import numpy as np
import matplotlib.pyplot as plt
from scipy.fftpack import fft, ifft, fftshift
import os

def solve_interference(N, t_target=75.0, filename="interference.png"):
    dx = 0.1
    L = N * dx
    x = dx * (np.arange(N) - 0.5 * N)
    
    dk = 2 * np.pi / L
    k = -N * dk / 2 + dk * np.arange(N)
    
    dt = 0.01
    
    hbar = 1.0
    p = hbar * k 
    m = 1.0
    
    a = 8.0
    x0 = -100.0
    E = 1.0
    k0 = np.sqrt(2 * m * E) / hbar
    
    def gaussian(x, a, x0, k0):
        return ((a * np.sqrt(np.pi))**(-0.5) * np.exp(-0.5 * ((x - x0) * 1. / a)**2 + 1j * x * k0))
        
    def potential(x):
        pot = 0 * x
        pot[x > 0] = 100.0 # potential wall
        return pot
        
    pot = potential(x)
    expV_half = np.exp(-1j * pot * dt / 2 / hbar)
    expV = expV_half * expV_half
    expT = fftshift(np.exp(-1j * p * p * dt / (2 * m) / hbar))
    
    psi = gaussian(x, a, x0, k0)
    
    t = 0.0
    while t < t_target:
        psi = ifft(expT * fft(expV * psi))
        t += dt
        
    plt.figure(figsize=(10, 6))
    plt.plot(x, np.abs(psi)**2, 'b-', label='$|\Psi(x,t)|^2$')
    plt.plot(x, 0.05 * pot, 'r-', label='Scaled Potential')
    plt.xlim(-50, 50)
    plt.ylim(0, 0.08)
    plt.xlabel('x')
    plt.ylabel('Probability Density')
    plt.title(f'Interference Pattern at t={t_target:.1f}, N=2^{int(np.log2(N))}')
    plt.legend(loc='upper left')
    plt.grid(True)
    plt.savefig("../report/" + filename)
    plt.close()

if __name__ == "__main__":
    solve_interference(2**13, filename="task1_interference_13.png")
    solve_interference(2**14, filename="task1_interference_14.png")
    print("Task 1 figures generated.")
