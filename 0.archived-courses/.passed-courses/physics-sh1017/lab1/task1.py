import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import quad

def f(theta, p, omega02=1):
    return -omega02 * np.sin(theta)

def rk4_step(theta, p, t, dt, omega02=1):
    xk1 = dt * p
    vk1 = dt * f(theta, p, omega02)
    xk2 = dt * (p + vk1 / 2)
    vk2 = dt * f(theta + xk1 / 2, p + vk1 / 2, omega02)
    xk3 = dt * (p + vk2 / 2)
    vk3 = dt * f(theta + xk2 / 2, p + vk2 / 2, omega02)
    xk4 = dt * (p + vk3)
    vk4 = dt * f(theta + xk3, p + vk3, omega02)
    theta += (xk1 + 2 * xk2 + 2 * xk3 + xk4) / 6
    p += (vk1 + 2 * vk2 + 2 * vk3 + vk4) / 6
    t += dt
    return theta, p, t

def get_period_simulation(theta0, dt=0.01):
    theta = theta0
    p = 0.0
    t = 0.0
    
    # Start: theta decreases. T/2 is when it starts increasing again.
    # To be more precise, we can find when p crosses zero or theta changes direction.
    # Since we start at theta0 with p=0, theta will decrease.
    # It will reach -theta0 and then start increasing.
    
    prev_theta = theta
    # Run a few steps to get away from start
    theta, p, t = rk4_step(theta, p, t, dt)
    
    while True:
        prev_theta = theta
        theta, p, t = rk4_step(theta, p, t, dt)
        if theta > prev_theta: # starts to increase
            return 2 * t
        if t > 100: # safety break
            return None

def period_integral(theta0):
    # T = 2 * sqrt(2) * integral_0^theta0 (1 / sqrt(cos(theta) - cos(theta0))) dtheta
    # To avoid singularity, use elliptic integral form or a small epsilon
    # Or just use the substitution theta = theta0 * sin(phi)
    # dtheta = theta0 * cos(phi) dphi
    func = lambda phi: 1.0 / np.sqrt(np.cos(theta0 * np.sin(phi)) - np.cos(theta0))
    # Actually, even with substitution it might be tricky.
    # Let's use the standard elliptic form: T = 4 * K(sin(theta0/2))
    from scipy.special import ellipk
    return 4 * ellipk(np.sin(theta0/2)**2) # ellipk takes m = k^2 in some libs, but in scipy it's m=k^2

def period_series(theta0):
    return 2 * np.pi * (1 + (1/16)*theta0**2 + (11/3072)*theta0**4)

def task1():
    theta0_values = np.linspace(0.1, np.pi - 0.1, 20)
    dts = [0.1, 0.01, 0.001]
    
    plt.figure(figsize=(10, 6))
    
    # Simulation for different dts
    for dt in dts:
        periods_sim = [get_period_simulation(th, dt) for th in theta0_values]
        plt.plot(theta0_values, periods_sim, 'o', label=f'Simulation ($\Delta t={dt}$)', markersize=4)
    
    # Analytical/Numerical integration
    periods_int = [period_integral(th) for th in theta0_values]
    plt.plot(theta0_values, periods_int, '-', label='Numerical Integration ($4K(k^2)$)', color='black')
    
    # Series expansion
    periods_ser = [period_series(th) for th in theta0_values]
    plt.plot(theta0_values, periods_ser, '--', label='Series Expansion')
    
    # Harmonic oscillator
    plt.axhline(y=2*np.pi, color='r', linestyle=':', label='Harmonic Oscillator ($2\pi$)')
    
    plt.xlabel(r'$\theta_0$ (rad)')
    plt.ylabel('Period $T$ (s)')
    plt.title('Period vs Initial Amplitude')
    plt.legend()
    plt.grid(True)
    plt.savefig('report/task1_period.png')
    # plt.show()

if __name__ == "__main__":
    task1()
