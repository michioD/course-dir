import numpy as np
import matplotlib.pyplot as plt

def shoot_ho(E, parity, N=1000):
    xmax = 5.0
    dx = xmax / N
    dx2 = dx**2
    x = 0.0
    
    if parity == 'even':
        psi = 1.0
        dpsi = 0.0
    else:
        psi = 0.0
        dpsi = 1.0
        
    x_tab = [x]
    psi_tab = [psi]
    
    for i in range(N):
        V_x = 0.5 * x**2
        V_next = 0.5 * (x+dx)**2
        d2psi = 2 * (V_x - E) * psi
        psi_new = psi + dpsi*dx + 0.5*d2psi*dx2
        d2psinew = 2 * (V_next - E) * psi_new
        dpsi += 0.5*(d2psi + d2psinew)*dx
        psi = psi_new
        x += dx
        x_tab.append(x)
        psi_tab.append(psi)
        
    return psi, x_tab, psi_tab

def find_eigenvalue_ho(E_min, E_max, parity, tol=1e-9):
    while (E_max - E_min) > tol:
        E_mid = (E_min + E_max) / 2
        psi_mid, _, _ = shoot_ho(E_mid, parity)
        psi_min, _, _ = shoot_ho(E_min, parity)
        if np.sign(psi_mid) == np.sign(psi_min):
            E_min = E_mid
        else:
            E_max = E_mid
    E_final = (E_min + E_max) / 2
    _, x_tab, psi_tab = shoot_ho(E_final, parity)
    return E_final, x_tab, psi_tab

searches = [
    (0.1, 1.0, 'even', 0),
    (1.0, 2.0, 'odd', 1),
    (2.0, 3.0, 'even', 2),
    (3.0, 4.0, 'odd', 3)
]

plt.figure(figsize=(10,6))
for E_min, E_max, parity, n in searches:
    E, x_tab, psi_tab = find_eigenvalue_ho(E_min, E_max, parity)
    print(f'n={n}, E_n={E:.2f}')
    plt.plot(x_tab, psi_tab, label=f'n={n}, E_n={E:.1f}')

# add dashed lines for psi=x and psi=1
x_line = np.linspace(0, 1, 100)
plt.plot(x_line, x_line, 'k:', label='$\psi=x$')
plt.axhline(1, color='k', ls=':', label='$\psi=1$')

plt.axhline(0, color='y', lw=1)
plt.xlabel('x')
plt.ylabel('$\psi$')
plt.title('First four eigenstates of a harmonic oscillator')
plt.xlim(0, 5)
plt.ylim(-2, 2)
plt.legend()
plt.savefig('report/p3_ho.png')
