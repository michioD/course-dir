import numpy as np
from matplotlib import pyplot as plt
from scipy.fftpack import fft, ifft, fftshift

# set x-axis scale
N = 2**13
dx = 0.1
L = N*dx
x = dx*(np.arange(N)-0.5*N)

# set momentum scale
dk = 2*np.pi/L
k = -N*dk/2 + dk*np.arange(N)

# time parameters
dt = 0.01
hbar = 1.0
p = hbar*k
m = 1.0

# Gaussian wave packet parameters
a = 8.0
x0 = -100.0
E = 1.0
k0 = np.sqrt(2*m*E)/hbar

def gaussian(x, a, x0, k0):
    return ((a*np.sqrt(np.pi))**(-0.5) * np.exp(-0.5*((x-x0)*1./a)**2 + 1j*x*k0))

def potential(x):
    pot = np.zeros_like(x)
    pot[x > 0] = 1000.0 # Infinite wall (high enough)
    return pot

pot = potential(x)
expV = np.exp(-1j*pot*dt/hbar)
expT = fftshift(np.exp(-1j*p*p*dt/(2*m)/hbar))

psi = gaussian(x, a, x0, k0)

times_to_plot = [0, 50, 100, 110, 120, 150]
plt.figure(figsize=(12, 8))

for i, t_val in enumerate(np.arange(0, 200, dt)):
    if any(np.isclose(t_val, t_target) for t_target in times_to_plot):
        plt.plot(x, np.abs(psi)**2, label=f't={t_val:.1f}')
    
    # SPO step
    # Note: The original code used expV_half * expV_half which is expV.
    # The symmetric split is: expV_half * expT * expV_half
    # But for a single step it's often approximated or we can do it properly.
    # Let's use the one in the original code: psi = ifft(expT*fft(expV*psi))
    psi = ifft(expT*fft(expV*psi))

plt.xlim(-150, 50)
plt.ylim(0, 0.1)
plt.xlabel('x')
plt.ylabel(r'$|\Psi(x,t)|^2$')
plt.title('Wave packet collision with an infinite wall')
plt.legend()
plt.savefig('report/q1_collision.png')
print("Saved report/q1_collision.png")
