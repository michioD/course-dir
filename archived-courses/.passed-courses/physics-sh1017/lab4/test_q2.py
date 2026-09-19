import numpy as np
from scipy.fftpack import fft, ifft, fftshift
import matplotlib.pyplot as plt

def run_simulation(E, t_target=None, get_psi=False):
    N = 2**14
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
    k0 = np.sqrt(2 * m * E) / hbar
    
    psi = ((a * np.sqrt(np.pi))**(-0.5) * np.exp(-0.5 * ((x - x0) * 1. / a)**2 + 1j * x * k0))
    
    pot = np.zeros_like(x)
    mask = x > 1.0
    pot[mask] = 1.0 / x[mask]
    
    expV_half = np.exp(-1j * pot * dt / 2 / hbar)
    expV = expV_half * expV_half
    expT = fftshift(np.exp(-1j * p * p * dt / (2 * m) / hbar))
    
    # Increase t_target significantly for low energies so they can emerge
    if t_target is None:
        t_target = 300.0 / np.sqrt(2 * E)
        
    t = 0.0
    while t < t_target:
        psi = ifft(expT * fft(expV * psi))
        t += dt
        
    # The barrier ends at x = 1/E. Let's measure Y_T strictly after that.
    x_end = 1.0 / E
    # Add a small buffer so we don't pick up the tail still inside
    Y_R = np.max(np.abs(psi[x <= 1.0]))
    Y_T = np.max(np.abs(psi[x > x_end + 5.0]))
    T = Y_T / (Y_R + Y_T)
    
    return T

energies = np.linspace(0.1, 0.9, 10) 
Ts = []
inv_sqrt_E = []

for E in energies:
    T = run_simulation(E)
    Ts.append(T)
    inv_sqrt_E.append(1.0 / np.sqrt(E))
    print(f"E={E:.2f}, T={T:.3e}")

ln_T = np.log(Ts)

plt.figure(figsize=(8, 6))
plt.plot(inv_sqrt_E, ln_T, 'ko-')
plt.xlabel('$1/\sqrt{E}$')
plt.ylabel('$\ln T$')
plt.title('Gamow Coulomb Barrier Transmission')
plt.grid(True)
plt.savefig("test_task2_gamow.png")
