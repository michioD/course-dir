import numpy as np
import matplotlib.pyplot as plt
from scipy.fftpack import fft, ifft, fftshift

def run_simulation(E, V0=5.0, t_target=None, get_psi=False):
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
    
    def gaussian(x, a, x0, k0):
        return ((a * np.sqrt(np.pi))**(-0.5) * np.exp(-0.5 * ((x - x0) * 1. / a)**2 + 1j * x * k0))
        
    def potential(x):
        C = 1.0
        R = 1.0
        pot = np.zeros_like(x)
        mask = x > R
        pot[mask] = C / x[mask]
        return pot
        
    pot = potential(x)
    expV_half = np.exp(-1j * pot * dt / 2 / hbar)
    expV = expV_half * expV_half
    expT = fftshift(np.exp(-1j * p * p * dt / (2 * m) / hbar))
    
    psi = gaussian(x, a, x0, k0)
    
    if t_target is None:
        t_target = 150.0 / np.sqrt(2 * E)
        
    t = 0.0
    while t < t_target:
        psi = ifft(expT * fft(expV * psi))
        t += dt
        
    if get_psi:
        return x, pot, psi
        
    # Calculate transmission probability (integral for x > 10)
    # T = np.sum(np.abs(psi[x > 10])**2) * dx
    # Calculate transmission probability using maximum amplitudes (Y_T, Y_R)
    Y_R = np.max(np.abs(psi[x <= 1.0]))
    Y_T = np.max(np.abs(psi[x > 1.0]))
    T = Y_T / (Y_R + Y_T)
    return T

def task2():
    # 1. Figure showing probability density splitting at Coulomb barrier
    print("Generating split figure...")
    E_split = 0.9       # Lower energy to < 1.0
    V0_split = 1.0      # Fix barrier to 1/x
    t_split = 110.0     # Give packet more time to separate
    x, pot, psi = run_simulation(E_split, V0=V0_split, t_target=t_split, get_psi=True)
    
    plt.figure(figsize=(10, 6))
    plt.plot(x, np.abs(psi)**2, 'b-', label='$|\Psi(x,t)|^2$')
    plt.plot(x, 0.05 * pot, 'r-', label='Scaled Potential')
    plt.xlim(-100, 100)
    plt.ylim(0, max(np.abs(psi)**2)*1.2)
    plt.xlabel('x')
    plt.ylabel('Probability Density')
    plt.title('Wave Packet Splitting at Coulomb Barrier')
    plt.legend()
    plt.grid(True)
    plt.savefig("task2_splitting.png")
    plt.close()
    
    # 2. Plot of ln(T) against 1/sqrt(E)
    print("Computing transmission probabilities...")
    # Sweep valid energies between 0 and 1
    energies = np.linspace(0.1, 0.9, 10)
    Ts = []
    inv_sqrt_E = []
    for E in energies:
        # Pass V0=1.0 for the correct barrier calculation
        T = run_simulation(E, V0=1.0)
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
    plt.savefig("task2_gamow.png")
    plt.close()

if __name__ == "__main__":
    task2()
    print("Task 2 figures generated.")
