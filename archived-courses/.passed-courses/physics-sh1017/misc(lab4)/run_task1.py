# -*- coding: utf-8 -*-
from simulation import SplitOperatorSimulation
import matplotlib.pyplot as plt
import numpy as np

def potential_wall(x):
    pot = np.zeros_like(x)
    pot[x > 0] = 100.0
    return pot

sim = SplitOperatorSimulation()
sim.set_potential(potential_wall)
sim.set_wave_packet(a=8.0, x0=-100.0, E=1.0)

# Initial state
plt.figure(figsize=(10, 6))
plt.plot(sim.x, sim.get_psi2(), label='Initial State (t=0)')
plt.plot(sim.x, 0.05 * sim.pot, 'r--', label='Potential (scaled)')
plt.xlim(-120, 20)
plt.ylim(0, 0.08)
plt.xlabel('x')
plt.ylabel('$|\Psi(x,t)|^2$')
plt.title('Task 1: Initial Wave Packet')
plt.legend()
plt.savefig('report/task1_initial.png')
plt.close()

# Intermediate state (moving towards wall)
sim.step(5000) # t = 50
plt.figure(figsize=(10, 6))
plt.plot(sim.x, sim.get_psi2(), label=f't={sim.t:.1f}')
plt.plot(sim.x, 0.05 * sim.pot, 'r--', label='Potential (scaled)')
plt.xlim(-120, 20)
plt.ylim(0, 0.08)
plt.xlabel('x')
plt.ylabel('$|\Psi(x,t)|^2$')
plt.title('Task 1: Wave Packet Moving Towards Wall')
plt.legend()
plt.savefig('report/task1_moving.png')
plt.close()

# Collision/Interference state
sim.step(4500) # t = 95
plt.figure(figsize=(10, 6))
plt.plot(sim.x, sim.get_psi2(), label=f't={sim.t:.1f}')
plt.plot(sim.x, 0.05 * sim.pot, 'r--', label='Potential (scaled)')
plt.xlim(-30, 10)
plt.ylim(0, 0.15)
plt.xlabel('x')
plt.ylabel('$|\Psi(x,t)|^2$')
plt.title('Task 1: Interference at Wall')
plt.legend()
plt.savefig('report/task1_interference.png')
plt.close()

# Reflected state
sim.step(5000) # t = 145
plt.figure(figsize=(10, 6))
plt.plot(sim.x, sim.get_psi2(), label=f't={sim.t:.1f}')
plt.plot(sim.x, 0.05 * sim.pot, 'r--', label='Potential (scaled)')
plt.xlim(-120, 20)
plt.ylim(0, 0.08)
plt.xlabel('x')
plt.ylabel('$|\Psi(x,t)|^2$')
plt.title('Task 1: Reflected Wave Packet')
plt.legend()
plt.savefig('report/task1_reflected.png')
plt.close()

print("Task 1 completed and plots saved.")
