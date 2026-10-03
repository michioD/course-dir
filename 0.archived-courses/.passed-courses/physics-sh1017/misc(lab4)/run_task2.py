# -*- coding: utf-8 -*-
from simulation import SplitOperatorSimulation
import matplotlib.pyplot as plt
import numpy as np

def potential_gamow(x):
    pot = np.zeros_like(x)
    mask = x > 1.0
    pot[mask] = 1.0 / x[mask]
    return pot

# Energy range to match Fig 4 plateau and slope
inv_sqrt_E_range = np.linspace(1.0, 3.2, 15)
energies = 1.0 / (inv_sqrt_E_range**2)
transmissions = []

for E in energies:
    sim = SplitOperatorSimulation(N=2**14, dx=0.1, dt=0.01) # Use higher resolution for low E
    sim.set_potential(potential_gamow)
    sim.set_wave_packet(a=8.0, x0=-60.0, E=E)
    
    v = np.sqrt(2*E)
    barrier_end = 1.0 / E
    # We want the packet to have reached well past the barrier
    t_end = (60.0 + barrier_end + 30.0) / v
    sim.step(int(t_end / sim.dt))
    
    psi2 = sim.get_psi2()
    # The reflected packet is at x < 1.0
    yr = np.max(psi2[sim.x < 0.0])
    # The transmitted packet is at x > barrier_end
    # We must be careful not to pick up the exponentially decaying tail inside the barrier
    # if the transmitted packet hasn't separated well. 
    # Actually, once the packet has tunneled, its max is a local peak past the barrier.
    # To be safe, look for the max amplitude for x > barrier_end + 10
    yt_region = psi2[sim.x > (barrier_end + 5.0)]
    if len(yt_region) > 0:
        yt = np.max(yt_region)
    else:
        yt = 1e-30 # Too far
    
    t_prob = yt / (yr + yt)
    transmissions.append(t_prob)
    print(f"1/sqrt(E)={1/np.sqrt(E):.2f}, E={E:.3f}, T={t_prob:.4e}, barrier_end={barrier_end:.1f}")

    if abs(1/np.sqrt(E) - 1.41) < 0.1:
        plt.figure(figsize=(8, 6))
        plt.plot(sim.x, sim.get_psi2(), color='blue', linewidth=1.0)
        plt.plot(sim.x, 0.05 * sim.pot, color='red', linewidth=1.0)
        plt.xlim(-100, 100)
        plt.ylim(0, 0.08)
        plt.xlabel('x')
        plt.ylabel('$|\Psi(x,t)|^2$')
        plt.savefig('report/task2_sim.png', bbox_inches='tight')
        plt.close()

ln_T = np.log(transmissions)

plt.figure(figsize=(8, 6))
plt.plot(inv_sqrt_E_range, ln_T, 'o-', markersize=4)
plt.xlabel('$1/\sqrt{E}$')
plt.ylabel('$\ln T$')
plt.title('Transmission Probability vs Energy')
plt.grid(True)
plt.savefig('report/task2_gamow_plot.png', bbox_inches='tight')
plt.close()

print("Task 2 updated.")
