import numpy as np
import matplotlib.pyplot as plt

def V(x):
    return 0.0

def solve_se(E, N):
    dx = 1.0/N
    dx2 = dx**2
    x = 0
    psi = 0
    dpsi = 1
    
    for i in range(N):
        d2psi = 2 * (V(x) - E) * psi
        d2psinew = 2 * (V(x + dx) - E) * (psi + dpsi * dx + 0.5 * d2psi * dx2)
        psi += dpsi * dx + 0.5 * d2psi * dx2
        dpsi += 0.5 * (d2psi + d2psinew) * dx
        x += dx
    return psi

E_exact = 0.5 * np.pi**2
Ns = [10, 100, 1000, 10000]
deltas = []

for N in Ns:
    delta = abs(solve_se(E_exact, N))
    deltas.append(delta)
    print(f"N={N}, delta={delta}")

plt.figure(figsize=(8,6))
plt.loglog(Ns, deltas, 'o-', label='Numerical Error $\Delta(N)$')
# Fit a line to verify slope -2
slope, intercept = np.polyfit(np.log(Ns), np.log(deltas), 1)
print(f"Slope of log-log plot: {slope}")

# Plot reference line constant/N^2
ref = deltas[0] * (Ns[0]**2) / (np.array(Ns)**2)
plt.loglog(Ns, ref, 'r--', label='Theoretical $1/N^2$')

plt.xlabel('N')
plt.ylabel('$\Delta = |\psi(1)|$')
plt.legend()
plt.title('Error scaling of Verlet method for Infinite Box')
plt.grid(True, which="both", ls="-")
plt.savefig('report/task1_error.png')
# plt.show()
