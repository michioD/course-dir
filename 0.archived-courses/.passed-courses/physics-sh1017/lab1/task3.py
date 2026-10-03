import numpy as np
import matplotlib.pyplot as plt

def f_driven(theta, p, t, gamma, A, omega, omega02=1):
    return -gamma * p + A * np.cos(omega * t) - omega02 * np.sin(theta)

def rk4_step_driven(theta, p, t, dt, gamma, A, omega, omega02=1):
    xk1 = dt * p
    vk1 = dt * f_driven(theta, p, t, gamma, A, omega, omega02)
    xk2 = dt * (p + vk1 / 2)
    vk2 = dt * f_driven(theta + xk1 / 2, p + vk1 / 2, t + dt/2, gamma, A, omega, omega02)
    xk3 = dt * (p + vk2 / 2)
    vk3 = dt * f_driven(theta + xk2 / 2, p + vk2 / 2, t + dt/2, gamma, A, omega, omega02)
    xk4 = dt * (p + vk3)
    vk4 = dt * f_driven(theta + xk3, p + vk3, t + dt, gamma, A, omega, omega02)
    theta += (xk1 + 2 * xk2 + 2 * xk3 + xk4) / 6
    p += (vk1 + 2 * vk2 + 2 * vk3 + vk4) / 6
    t += dt
    while theta > np.pi: theta -= 2 * np.pi
    while theta < -np.pi: theta += 2 * np.pi
    return theta, p, t

def get_steady_state(gamma, A, omega, t_max=1000, dt=0.01):
    theta = 0.0
    p = 0.0
    t = 0.0
    
    prev_max = 0
    thetas = []
    
    for _ in range(int(t_max/dt)):
        theta, p, t = rk4_step_driven(theta, p, t, dt, gamma, A, omega)
        thetas.append(theta)
        
        # Check for steady state every few periods
        if len(thetas) > 2000 and len(thetas) % 1000 == 0:
            recent = thetas[-1000:]
            current_max = np.max(recent)
            if abs(current_max - prev_max) < 1e-6:
                return (np.max(recent) - np.min(recent)) / 2
            prev_max = current_max
            
    return (np.max(thetas[-1000:]) - np.min(thetas[-1000:])) / 2

def task3():
    gamma = 3/8
    omega = 2/3
    
    # Range of A values as in example (0.1 to 0.8)
    A_values = np.linspace(0.1, 0.8, 40)
    steady_amps = [get_steady_state(gamma, a, omega) for a in A_values]
    
    plt.figure(figsize=(10, 6))
    plt.plot(A_values, steady_amps, 'bo-', markersize=4)
    plt.xlabel('Drive force amplitude A')
    plt.ylabel('Steady state amplitude')
    plt.title('Steady State Against Drive Force')
    plt.grid(True)
    plt.savefig('report/task3_steady_state_vs_A.png')
    
    # A = 1.0 case
    A = 1.0
    theta, p, t = 0, 0, 0
    dt = 0.01
    all_theta = []
    all_p = []
    for _ in range(int(1000/dt)):
        theta, p, t = rk4_step_driven(theta, p, t, dt, gamma, A, omega)
        if t > 200: # skip transients
            all_theta.append(theta)
            all_p.append(p)
            
    plt.figure(figsize=(8, 8))
    plt.plot(all_theta, all_p, 'b,', alpha=0.5)
    plt.xlabel(r'$\theta$')
    plt.ylabel('p')
    plt.title('System when A=1')
    plt.grid(True)
    plt.savefig('report/task3_A1_phase.png')

if __name__ == "__main__":
    task3()
