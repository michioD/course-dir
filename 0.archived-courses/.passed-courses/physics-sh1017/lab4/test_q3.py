import numpy as np
from scipy.fftpack import fft, ifft, fftshift

def run_simulation_q3(V_type, V0=1.0, E=0.5, t_target=150.0):
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
    a = 10.0
    x0 = -100.0
    k0 = np.sqrt(2 * m * E) / hbar
    
    psi = ((a * np.sqrt(np.pi))**(-0.5) * np.exp(-0.5 * ((x - x0) * 1. / a)**2 + 1j * x * k0))
    pot = np.zeros_like(x)
    if V_type == 'slanted':
        L_barrier = 4.0
        mask = (x > 0) & (x < L_barrier)
        pot[mask] = V0 * (1.0 - x[mask] / L_barrier)
        
    expV_half = np.exp(-1j * pot * dt / 2 / hbar)
    expV = expV_half * expV_half
    expT = fftshift(np.exp(-1j * p * p * dt / (2 * m) / hbar))
    
    t = 0.0
    while t < t_target:
        psi = ifft(expT * fft(expV * psi))
        t += dt
        
    T_amp = np.max(np.abs(psi[x > 4.0])) / (np.max(np.abs(psi[x <= 0.0])) + np.max(np.abs(psi[x > 4.0])))
    T_int = np.sum(np.abs(psi[x > 4.0])**2) * dx
    return T_amp, T_int

for V0 in [0.6, 0.7, 0.8, 0.9, 1.0]:
    Ta, Ti = run_simulation_q3('slanted', V0)
    print(f"V0={V0:.1f}, T_amp={Ta:.4f}, ln(Ta)={np.log(Ta):.4f}, T_int={Ti:.4f}, ln(Ti)={np.log(Ti):.4f}")
