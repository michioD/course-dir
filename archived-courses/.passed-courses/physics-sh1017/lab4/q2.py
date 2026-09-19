import numpy as np
import matplotlib.pyplot as plt
from scipy.fftpack import fft, ifft, fftshift

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
    
    def gaussian(x, a, x0, k0):
        return ((a * np.sqrt(np.pi))**(-0.5) * np.exp(-0.5 * ((x - x0) * 1. / a)**2 + 1j * x * k0))
        
    def potential(x):
        pot = np.zeros_like(x)
        # R = 1.0, C = 1.0 according to Gamow's alpha decay theory
        mask = x > 1.0
        pot[mask] = 1.0 / x[mask]
        return pot
        
    pot = potential(x)
    expV_half = np.exp(-1j * pot * dt / 2 / hbar)
    expV = expV_half * expV_half
    expT = fftshift(np.exp(-1j * p * p * dt / (2 * m) / hbar))
    
    psi = gaussian(x, a, x0, k0)
    
    # Allow enough time for the packet to hit the barrier and separate
    if t_target is None:
        t_target = 300.0 / np.sqrt(2 * E)
        
    t = 0.0
    while t < t_target:
        psi = ifft(expT * fft(expV * psi))
        t += dt
        
    if get_psi:
        return x, pot, psi
        
    # Calculate transmission probability using maximum amplitudes (Y_T, Y_R)
    # The barrier starts at x = 1.0. For the transmitted packet, we must measure 
    # strictly after the barrier ends at x = 1/E to avoid picking up the evanescent tail.
    x_end = 1.0 / E
    Y_R = np.max(np.abs(psi[x <= 1.0]))
    Y_T = np.max(np.abs(psi[x > x_end + 5.0]))
    T = Y_T / (Y_R + Y_T)
    
    return T

def task2():
    # 1. Figure showing probability density splitting at Coulomb barrier
    print("Generating split figure...")
    E_split = 0.9       # Energy < 1.0
    t_split = 110.0     # Time when wave packet is hitting the barrier
    x, pot, psi = run_simulation(E_split, t_target=t_split, get_psi=True)
    
    plt.figure(figsize=(10, 6))
    plt.plot(x, np.abs(psi)**2, 'b-', label='$|\Psi(x,t)|^2$')
    plt.plot(x, 0.05 * pot, 'r-', label='Potential (Scaled $\\times 0.05$)')
    plt.xlim(-100, 100)
    
    # Set y-limit slightly above the peak of the scaled potential (0.05) 
    # so the red boundary line is fully rendered in the plot
    plt.ylim(0, 0.06)
    
    plt.xlabel('x')
    plt.ylabel('Probability Density')
    plt.title('Wave Packet Splitting at Coulomb Barrier')
    plt.legend()
    plt.grid(True)
    plt.savefig("task2_splitting.png")
    plt.close()
    
    # 2. Plot of ln(T) against 1/sqrt(E)
    print("Computing transmission probabilities...")
    # Energies bounded between 0.1 and 0.9
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
    plt.savefig("task2_gamow.png")
    plt.close()

if __name__ == "__main__":
    task2()
    print("Task 2 figures generated.")