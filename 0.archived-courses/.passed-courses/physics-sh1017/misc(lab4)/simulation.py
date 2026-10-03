# -*- coding: utf-8 -*-
import numpy as np
from matplotlib import pyplot as plt
from scipy.fftpack import fft, ifft, fftshift

class SplitOperatorSimulation:
    def __init__(self, N=2**13, dx=0.1, dt=0.01, hbar=1.0, m=1.0):
        self.N = N
        self.dx = dx
        self.L = N * dx
        self.dt = dt
        self.hbar = hbar
        self.m = m
        
        self.x = dx * (np.arange(N) - 0.5 * N)
        self.dk = 2 * np.pi / self.L
        self.k = -N * self.dk / 2 + self.dk * np.arange(N)
        self.p = hbar * self.k
        
        self.t = 0.0
        self.psi = None
        self.pot = None
        self.expV = None
        self.expT = fftshift(np.exp(-1j * self.p**2 * dt / (2 * self.m) / hbar))

    def set_potential(self, pot_func):
        self.pot = pot_func(self.x)
        self.expV = np.exp(-1j * self.pot * self.dt / self.hbar)

    def set_wave_packet(self, a, x0, E):
        k0 = np.sqrt(2 * self.m * E) / self.hbar
        self.psi = ((a * np.sqrt(np.pi))**(-0.5) * 
                    np.exp(-0.5 * ((self.x - x0) / a)**2 + 1j * self.x * k0))

    def step(self, nsteps=1):
        for _ in range(nsteps):
            # Standard SPO: psi = exp(-iV dt/2) exp(-iT dt) exp(-iV dt/2) psi
            # But the original code used a simpler one-step:
            # psi = ifft(expT * fft(expV * psi))
            # which is equivalent to exp(-iT dt) exp(-iV dt)
            self.psi = ifft(self.expT * fft(self.expV * self.psi))
            self.t += self.dt

    def get_psi2(self):
        return np.abs(self.psi)**2

    def get_transmission_reflection(self, barrier_x):
        psi2 = self.get_psi2()
        transmission = np.sum(psi2[self.x > barrier_x]) * self.dx
        reflection = np.sum(psi2[self.x <= barrier_x]) * self.dx
        return transmission, reflection
