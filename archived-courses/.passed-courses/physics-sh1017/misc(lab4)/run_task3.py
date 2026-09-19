# -*- coding: utf-8 -*-
from simulation import SplitOperatorSimulation
import matplotlib.pyplot as plt
import numpy as np

def potential_step(x):
    pot = np.zeros_like(x)
    pot[x > 0] = 1.0
    return pot

# Match Fig 5
sim = SplitOperatorSimulation(dt=0.01)
sim.set_potential(potential_step)
# Use a=8 for Task 3 to match the peak height in Fig 5 (around 0.03-0.04)
sim.set_wave_packet(a=8.0, x0=-35.0, E=0.9)

# Run until near step
sim.step(int(15.0 / sim.dt))

plt.figure(figsize=(8, 6))
plt.plot(sim.x, sim.get_psi2(), color='blue', linewidth=0.5)
plt.plot(sim.x, 0.05 * sim.pot, color='red', linewidth=1)
plt.xlim(-100, 100)
plt.ylim(0, 0.08)
plt.xlabel('x')
plt.ylabel('$|\Psi(x,t)|^2$')
plt.xticks([-100, -75, -50, -25, 0, 25, 50, 75, 100])
plt.savefig('report/task3_step.png', bbox_inches='tight')
plt.close()

# Match Fig 6
L = 4.0
# V0 values to get V0^3/2 range ~0.45 to 1.0
V0_values = np.linspace(0.6, 1.0, 5)
transmissions = []

for V0 in V0_values:
    def potential_triangular(x):
        pot = np.zeros_like(x)
        mask = (x > 0) & (x < L)
        pot[mask] = V0 * (1 - x[mask] / L)
        return pot
    
    sim = SplitOperatorSimulation(dt=0.01)
    sim.set_potential(potential_triangular)
    sim.set_wave_packet(a=8.0, x0=-40.0, E=0.5)
    
    v = np.sqrt(2*0.5)
    t_end = 100.0 / v
    sim.step(int(t_end / sim.dt))
    
    psi2 = sim.get_psi2()
    yr = np.max(psi2[sim.x < 0.0])
    yt = np.max(psi2[sim.x > L])
    t_prob = yt / (yr + yt)
    transmissions.append(t_prob)

V0_32 = V0_values**1.5
ln_T = np.log(transmissions)

plt.figure(figsize=(8, 6))
plt.plot(V0_32, ln_T, 'ro-', markersize=5)
plt.xlabel('$V_0^{(3/2)}$') # Match Fig 6 label exactly
plt.ylabel('$\ln T$')
plt.title('$V_0$') # Weird title in example but matching
plt.grid(True)
plt.savefig('report/task3_fn_plot.png', bbox_inches='tight')
plt.close()

print("Task 3 updated.")
