import numpy as np
from matplotlib import pyplot as plt
from scipy.fftpack import fft, ifft, fftshift

# set x-axis scale
N = 2**13
dx = 0.05
L = N*dx
x = dx*(np.arange(N)-0.5*N)

# set momentum scale
dk = 2*np.pi/L
k = -N*dk/2 + dk*np.arange(N)

# parameters
dt = 0.01
hbar = 1.0
m = 1.0
p = hbar*k

def gaussian(x, a, x0, k0):
    return ((a*np.sqrt(np.pi))**(-0.5) * np.exp(-0.5*((x-x0)*1./a)**2 + 1j*x*k0))

def potential(x):
    pot = np.zeros_like(x)
    # V0 = 0, R = 1, C = 1
    # V(x) = -V0 for x < R
    # V(x) = C/x for x > R
    # To prevent division by zero and handle the step
    mask = (x >= 1.0)
    pot[mask] = 1.0 / x[mask]
    pot[~mask] = 0.0
    return pot

pot = potential(x)
expV = np.exp(-1j*pot*dt/hbar)
expT = fftshift(np.exp(-1j*p*p*dt/(2*m)/hbar))

energies = np.linspace(0.1, 0.9, 9)
transmissions = []

for E in energies:
    k0 = np.sqrt(2*m*E)/hbar
    a = 5.0
    x0 = -10.0 # Start inside but enough space to form the packet
    psi = gaussian(x, a, x0, k0)
    
    # We need to run until the packet has split and separated
    # tmax depends on E (velocity v = k0*hbar/m)
    v = k0 * hbar / m
    # Distance to cover: from x0=-10 to x=0 is 10, then it needs to separate.
    # Let's say we run for t = 40 / v
    tmax = 60.0 / v
    
    for _ in range(int(tmax/dt)):
        psi = ifft(expT*fft(expV*psi))
    
    # Calculate amplitudes
    psi2 = np.abs(psi)**2
    # Transmitted is x > 1 (approx)
    # Reflected is x < 1 (approx)
    # But we want max amplitudes YT, YR as per instructions
    # "YT, YR maxamplituden hos det transmitterade och reflekterade vågpaketet"
    
    # Separate the packets
    # Reflected packet should be moving left
    # Transmitted packet should be moving right
    
    # Find peak in x > 5 and peak in x < -5 to be safe
    mask_T = (x > 5.0)
    mask_R = (x < -5.0)
    
    YT = np.max(psi2[mask_T]) if any(mask_T) else 0
    YR = np.max(psi2[mask_R]) if any(mask_R) else 0
    
    T = YT / (YR + YT) if (YR + YT) > 0 else 0
    transmissions.append(T)
    print(f"E={E:.2f}, T={T:.4f}")

plt.figure(figsize=(10, 6))
inv_sqrt_E = 1.0 / np.sqrt(energies)
plt.plot(inv_sqrt_E, np.log(transmissions), 'o-')
plt.xlabel(r'$1/\sqrt{E}$')
plt.ylabel(r'$\ln T$')
plt.title('Gamow Theory: Transmission Probability vs Energy')
plt.grid(True)
plt.savefig('report/q2_gamow.png')
print("Saved report/q2_gamow.png")

# Also save a sample plot for E=0.5
E = 0.5
k0 = np.sqrt(2*m*E)/hbar
psi = gaussian(x, a, x0, k0)
tmax = 60.0 / (k0 * hbar / m)
for _ in range(int(tmax/dt)):
    psi = ifft(expT*fft(expV*psi))
plt.figure()
plt.plot(x, np.abs(psi)**2)
plt.xlim(-100, 100)
plt.title(f'Wave packet after tunneling (E={E})')
plt.savefig('report/q2_sample_packet.png')
