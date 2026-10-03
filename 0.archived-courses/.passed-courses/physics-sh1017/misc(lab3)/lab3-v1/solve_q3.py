import numpy as np
from matplotlib import pyplot as plt
from scipy.fftpack import fft, ifft, fftshift

# set x-axis scale
N = 2**13
dx = 0.05
L_total = N*dx
x = dx*(np.arange(N)-0.5*N)

# set momentum scale
dk = 2*np.pi/L_total
k = -N*dk/2 + dk*np.arange(N)

# parameters
dt = 0.01
hbar = 1.0
m = 1.0
p = hbar*k

def gaussian(x, a, x0, k0):
    return ((a*np.sqrt(np.pi))**(-0.5) * np.exp(-0.5*((x-x0)*1./a)**2 + 1j*x*k0))

# Part 1: Potential Step
def potential_step(x, V0=1.0):
    pot = np.zeros_like(x)
    pot[x > 0] = V0
    return pot

# Part 2: Fowler-Nordheim Potential
def potential_fn(x, V0, L=4.0):
    pot = np.zeros_like(x)
    # V(x) = 0 for x < 0
    # V(x) = V0(1 - x/L) for 0 < x < L
    # V(x) = 0 for x > L
    mask_barrier = (x >= 0) & (x <= L)
    pot[mask_barrier] = V0 * (1.0 - x[mask_barrier] / L)
    return pot

# Demonstrate Step Reflection
V0_step = 1.0
k0 = 1.0 # E = 0.5 * 1^2 / 1 = 0.5 < V0
a = 10.0
x0 = -50.0
psi = gaussian(x, a, x0, k0)
pot = potential_step(x, V0_step)
expV = np.exp(-1j*pot*dt/hbar)
expT = fftshift(np.exp(-1j*p*p*dt/(2*m)/hbar))

for _ in range(int(150.0/dt)):
    psi = ifft(expT*fft(expV*psi))

plt.figure()
plt.plot(x, np.abs(psi)**2)
plt.title(f'Reflection at potential step (V0=1, E=0.5)')
plt.xlim(-150, 50)
plt.savefig('report/q3_step_reflection.png')

# Demonstrate FN Tunneling
L_field = 4.0
psi = gaussian(x, a, x0, k0)
pot = potential_fn(x, V0_step, L_field)
expV = np.exp(-1j*pot*dt/hbar)

for _ in range(int(150.0/dt)):
    psi = ifft(expT*fft(expV*psi))

plt.figure()
plt.plot(x, np.abs(psi)**2)
plt.title(f'Fowler-Nordheim Tunneling (V0=1, E=0.5, L=4)')
plt.xlim(-150, 150)
plt.savefig('report/q3_fn_tunneling.png')

# Investigate ln T vs V0^(3/2)
v0_values = np.arange(0.6, 1.3, 0.1)
transmissions = []
E = 0.4 # Fixed E < V0
k0 = np.sqrt(2*m*E)/hbar

for v0 in v0_values:
    psi = gaussian(x, a, x0, k0)
    pot = potential_fn(x, v0, L_field)
    expV = np.exp(-1j*pot*dt/hbar)
    
    # Run until packets separate
    v = k0 * hbar / m
    tmax = 120.0 / v
    for _ in range(int(tmax/dt)):
        psi = ifft(expT*fft(expV*psi))
    
    psi2 = np.abs(psi)**2
    # Find peaks
    mask_T = (x > L_field + 5.0)
    mask_R = (x < -10.0)
    YT = np.max(psi2[mask_T]) if any(mask_T) else 0
    YR = np.max(psi2[mask_R]) if any(mask_R) else 0
    T = YT / (YR + YT) if (YR + YT) > 0 else 0
    transmissions.append(T)
    print(f"V0={v0:.1f}, T={T:.4f}")

plt.figure()
plt.plot(v0_values**1.5, np.log(transmissions), 'o-')
plt.xlabel(r'$V_0^{3/2}$')
plt.ylabel(r'$\ln T$')
plt.title('Fowler-Nordheim: Transmission vs $V_0^{3/2}$')
plt.grid(True)
plt.savefig('report/q3_fn_scaling.png')
