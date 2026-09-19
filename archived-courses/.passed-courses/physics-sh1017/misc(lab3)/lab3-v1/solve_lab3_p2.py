import numpy as np
import matplotlib.pyplot as plt

def shoot_box(E, N=10000):
    dx = 1.0 / N
    dx2 = dx**2
    x = 0.0
    psi = 0.0
    dpsi = 1.0
    
    x_tab = [x]
    psi_tab = [psi]
    
    for i in range(N):
        d2psi = -2 * E * psi
        psi_new = psi + dpsi*dx + 0.5*d2psi*dx2
        d2psinew = -2 * E * psi_new
        dpsi += 0.5*(d2psi + d2psinew)*dx
        psi = psi_new
        x += dx
        x_tab.append(x)
        psi_tab.append(psi)
        
    return psi, x_tab, psi_tab

def find_eigenvalue(E_min, E_max, tol=1e-9):
    while (E_max - E_min) > tol:
        E_mid = (E_min + E_max) / 2
        psi_mid, _, _ = shoot_box(E_mid)
        psi_min, _, _ = shoot_box(E_min)
        if np.sign(psi_mid) == np.sign(psi_min):
            E_min = E_mid
        else:
            E_max = E_mid
    E_final = (E_min + E_max) / 2
    _, x_tab, psi_tab = shoot_box(E_final)
    return E_final, x_tab, psi_tab

energies = []
eigenstates = []

intervals = [(0.1, 10), (10, 30), (30, 60), (60, 100)]
for E_min, E_max in intervals:
    E, x_tab, psi_tab = find_eigenvalue(E_min, E_max)
    energies.append(E)
    psi_tab = np.array(psi_tab)
    norm = np.sqrt(np.sum(psi_tab**2) * (1.0/10000))
    eigenstates.append((x_tab, psi_tab/norm))

plt.figure(figsize=(10,6))
for i, (E, (x_tab, psi_tab)) in enumerate(zip(energies, eigenstates)):
    n = i + 1
    plt.plot(x_tab, psi_tab, label=f'n={n}, E_n={E:.2f}')
    print(f'n={n} with E = {E:.3f}')

plt.axhline(0, color='y', lw=1)
plt.axvline(0, color='y', ls=':')
plt.axvline(1, color='y', ls=':')
plt.xlabel('x')
plt.ylabel('$\psi$')
plt.title('Eigenstates for n=1,2,3,4 and their corresponding eigenvalue energies')
plt.legend()
plt.savefig('report/p2_eigenstates.png')
