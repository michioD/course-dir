import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import linregress

def f_damped(theta, p, t, gamma, omega02=1):
    return -gamma * p - omega02 * np.sin(theta)

def rk4_step_damped(theta, p, t, dt, gamma, omega02=1):
    xk1 = dt * p
    vk1 = dt * f_damped(theta, p, t, gamma, omega02)
    xk2 = dt * (p + vk1 / 2)
    vk2 = dt * f_damped(theta + xk1 / 2, p + vk1 / 2, t + dt/2, gamma, omega02)
    xk3 = dt * (p + vk2 / 2)
    vk3 = dt * f_damped(theta + xk2 / 2, p + vk2 / 2, t + dt/2, gamma, omega02)
    xk4 = dt * (p + vk3)
    vk4 = dt * f_damped(theta + xk3, p + vk3, t + dt, gamma, omega02)
    theta += (xk1 + 2 * xk2 + 2 * xk3 + xk4) / 6
    p += (vk1 + 2 * vk2 + 2 * vk3 + vk4) / 6
    t += dt
    return theta, p, t

def simulate_damped(theta0, gamma, dt=0.01, t_max=40):
    theta = theta0
    p = 0.0
    t = 0.0
    
    times = [t]
    thetas = [theta]
    turning_points_t = [0]
    turning_points_theta = [theta0]
    
    while t < t_max:
        prev_p = p
        theta, p, t = rk4_step_damped(theta, p, t, dt, gamma)
        times.append(t)
        thetas.append(theta)
        
        if prev_p * p < 0: # Turning point
            fraction = -prev_p / (p - prev_p)
            t_tp = (t - dt) + fraction * dt
            theta_tp = thetas[-2] + fraction * (theta - thetas[-2])
            turning_points_t.append(t_tp)
            turning_points_theta.append(theta_tp)
            
    return np.array(times), np.array(thetas), np.array(turning_points_t), np.array(turning_points_theta)

def task2():
    theta0 = np.pi/2 # Following example report's theta0
    gamma = 1.0
    times, thetas, tp_t, tp_theta = simulate_damped(theta0, gamma, t_max=40)
    
    # Take positive amplitudes only for log fit
    pos_tp_t = tp_t[::2] # Initial, 2nd turn, 4th turn... (local maxima)
    pos_tp_theta = tp_theta[::2]
    
    # Linear fit to log(amplitude)
    log_amps = np.log(np.abs(pos_tp_theta))
    slope, intercept, r_value, p_value, std_err = linregress(pos_tp_t, log_amps)
    
    # Fit function: ln(A) = slope * t + intercept
    # A(t) = exp(intercept) * exp(slope * t)
    fit_label = f'Linear Fit: $\ln A(t) = {slope:.2f}t + {intercept:.2f}$'
    
    plt.figure(figsize=(10, 6))
    plt.plot(pos_tp_t, log_amps, 'bo', label='Log of Swing Amplitudes')
    plt.plot(pos_tp_t, slope * pos_tp_t + intercept, 'r--', label=fit_label)
    plt.xlabel('Time (s)')
    plt.ylabel('Logarithm of Amplitude (log(rad))')
    plt.title('Logarithmic plot of swing amplitude vs. time for damped system')
    plt.legend()
    plt.grid(True)
    plt.savefig('report/task2_log_fit.png')
    
    # Characteristic time tau = ln(2) / lambda where lambda = -slope
    decay_const = -slope
    tau = np.log(2) / decay_const
    print(f"Decay constant lambda: {decay_const:.4f}")
    print(f"Characteristic time tau: {tau:.4f} s")

    # Overdamping threshold investigation
    gammas = np.linspace(0.1, 2.5, 30)
    first_turn_amps = []
    for g in gammas:
        _, _, _, tp_th = simulate_damped(np.pi/2, g, t_max=20)
        if len(tp_th) > 1:
            first_turn_amps.append(np.abs(tp_th[1]))
        else:
            first_turn_amps.append(0)

    plt.figure(figsize=(12, 5))
    plt.subplot(1, 2, 1)
    plt.plot(gammas, first_turn_amps, 'b-')
    plt.xlabel(r'$\gamma$')
    plt.ylabel('Amplitude of the first turn (rad)')
    plt.title(r'Amplitude of the first turn vs $\gamma$')
    plt.grid(True)

    plt.subplot(1, 2, 2)
    plt.plot(1/gammas, first_turn_amps, 'b-')
    plt.xlabel(r'$1/\gamma$')
    plt.ylabel('Amplitude of the first turn (rad)')
    plt.title(r'Amplitude of the first turn vs $1/\gamma$')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('report/task2_first_turn_comparison.png')

if __name__ == "__main__":
    task2()
