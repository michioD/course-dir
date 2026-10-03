import numpy as np
import matplotlib.pyplot as plt

E = 0.5 * np.pi**2

def solve_box(N):
    dx = 1.0 / N
    dx2 = dx**2
    x = 0.0
    psi = 0.0
    dpsi = 1.0
    for i in range(N):
        d2psi = -2 * E * psi
        psi_new = psi + dpsi*dx + 0.5*d2psi*dx2
        d2psinew = -2 * E * psi_new
        dpsi += 0.5*(d2psi + d2psinew)*dx
        psi = psi_new
        x += dx
    return abs(psi)

Ns = [10, 100, 1000, 10000]
deltas = [solve_box(N) for N in Ns]

plt.figure(figsize=(8,6))
plt.loglog(Ns, deltas, 'o-', label='Computed $\Delta$')
constant = deltas[0] * Ns[0]**2
plt.loglog(Ns, [constant/N**2 for N in Ns], 'r--', label='Theoretical $\Delta = constant/N^2$')
plt.xlabel('Number of Mesh Points (N)')
plt.ylabel('Error $\Delta = |\psi(1)|$')
plt.title('Error Analysis on Log-Log Scale')
plt.legend()
plt.grid(True, which="both", ls="--")
plt.savefig('report/p1_error.png')
print("P1 Deltas:", deltas)
