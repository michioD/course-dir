# -*- coding: utf-8 -*-
from simulation import SplitOperatorSimulation
import matplotlib.pyplot as plt
import numpy as np

def potential_wall(x):
    pot = np.zeros_like(x)
    pot[x > 0] = 100.0
    return pot

# Match Task 1 figures exactly to Fig 1 & 2
for N in [2**13, 2**14]:
    sim = SplitOperatorSimulation(N=N, dx=0.1)
    sim.set_potential(potential_wall)
    sim.set_wave_packet(a=8.0, x0=-100.0, E=1.0)
    
    # Run until interference at the wall (t ~ 95)
    sim.step(int(95.0 / sim.dt))
    
    plt.figure(figsize=(8, 6))
    plt.plot(sim.x, sim.get_psi2(), color='blue', linewidth=0.5)
    plt.xlim(-100, 100)
    plt.ylim(0, 0.08)
    plt.xlabel('x')
    plt.ylabel('$|\Psi(x,t)|^2$')
    # Use standard ticks to match example
    plt.xticks([-100, -75, -50, -25, 0, 25, 50, 75, 100])
    plt.yticks([0.00, 0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08])
    plt.savefig(f'report/task1_N{N}.png', bbox_inches='tight', dpi=150)
    plt.close()

print("Task 1 updated.")
