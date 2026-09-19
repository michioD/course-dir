import numpy as np
import matplotlib.pyplot as plt
from scipy.fftpack import fft, ifft, fftshift

def run_simulation_q3(V_type, V0=1.0, E=0.5, t_target=None, get_psi=False):
    N = 2**14
    dx = 0.1
    L_domain = N * dx
    x = dx * (np.arange(N) - 0.5 * N)
    
    dk = 2 * np.pi / L_domain
    k = -N * dk / 2 + dk * np.arange(N)
    
    dt = 0.01
    
    hbar = 1.0
    p = hbar * k 
    m = 1.0
    
    # Lab instructions specify a=10 and k0=1 for Question 3
    a = 10.0
    x0 = -100.0
    k0 = np.sqrt(2 * m * E) / hbar
    
    def gaussian(x, a, x0, k0):
        return ((a * np.sqrt(np.pi))**(-0.5) * np.exp(-0.5 * ((x - x0) * 1. / a)**2 + 1j * x * k0))
        
    def potential(x):

        pot = np.zeros_like(x)
        if V_type == 'step':
            # Flat potential step: V0 for x > 0
            pot[x > 0] = V0
        elif V_type == 'slanted':
            # Electric field potential: V0(1 - x/L) for 0 < x < L
            L_barrier = 4.0
            mask = (x > 0) & (x < L_barrier)
            pot[mask] = V0 * (1.0 - x[mask] / L_barrier)
            # pot is 0 for x > L
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
        
    # Calculate transmission probability 
    # For the slanted barrier, we measure transmission past L=4
    Y_R = np.max(np.abs(psi[x <= 0.0]))
    Y_T = np.max(np.abs(psi[x > 4.0]))
    T = Y_T / (Y_R + Y_T)
    
    return T

def task3():
    # We use E = 0.5 because the lab specifies k0 = 1, and E = (hbar*k0)^2 / 2m
    E_electron = 0.5 
    
    # 1. Figure showing total reflection at a potential step
    print("Generating potential step reflection figure...")
    t_reflect = 110.0 # Time when wave packet has bounced off the step
    x, pot, psi = run_simulation_q3(V_type='step', V0=1.0, E=E_electron, t_target=t_reflect, get_psi=True)
    
    plt.figure(figsize=(10, 6))
    plt.plot(x, np.abs(psi)**2, 'b-', label='$|\Psi(x,t)|^2$')
    plt.plot(x, 0.05 * pot, 'r-', label='Scaled Potential')
    plt.xlim(-100, 100)
    plt.ylim(0, max(np.abs(psi)**2)*1.2)
    plt.xlabel('x')
    plt.ylabel('Probability Density')
    plt.title('Total Reflection at Potential Step ($E < V_0$)')
    plt.legend()
    plt.grid(True)
    plt.savefig("task3_reflection.png")
    plt.close()
    
    # 2. Plot of ln(T) against V0^(3/2) for Fowler-Nordheim Tunneling
    print("Computing Fowler-Nordheim transmission probabilities...")
    V0_vals = np.array([0.6, 0.7, 0.8, 0.9, 1.0])
    Ts = []
    V0_32 = []
    
    for V0 in V0_vals:
        T = run_simulation_q3(V_type='slanted', V0=V0, E=E_electron)
        Ts.append(T)
        V0_32.append(V0**1.5)
        print(f"V0={V0:.1f}, T={T:.3e}")
        
    ln_T = np.log(Ts)
    
    plt.figure(figsize=(8, 6))
    plt.plot(V0_32, ln_T, 'ko-')
    plt.xlabel('$V_0^{3/2}$')
    plt.ylabel('$\ln T$')
    plt.title('Fowler-Nordheim Tunneling (Field Emission)')
    plt.grid(True)
    plt.savefig("task3_fowler_nordheim.png")
    plt.close()

if __name__ == "__main__":
    task3()
    print("Task 3 figures generated.")