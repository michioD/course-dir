import numpy as np
import matplotlib.pyplot as plt
import os

def simulate_doubleslit(wavelength=0.0005, d=0.5, D=2000, W=50, points=2000, filename=None):
    k = 2*np.pi/wavelength
    x1 = d/2
    x2 = -d/2

    screen_x = np.linspace(-W/2, W/2, points)
    intensity = np.empty(points)
    
    for i, x in enumerate(screen_x):
        r = np.sqrt(D**2 + x**2)
        r1 = np.sqrt(D**2 + (x-x1)**2)
        r2 = np.sqrt(D**2 + (x-x2)**2)
        # Formula from PDF: E^2 = (|A|^2/r^2) * (N/2 + sum cos(k|r-ri| - k|r-rj|))
        # For N=2: E^2 = (|A|^2/r^2) * (1 + cos(k(r1-r2)))
        intensity[i] = (1 + np.cos(k*(r1-r2)))/r**2

    # Normalize for plotting comparison
    intensity_norm = intensity / np.max(intensity)
    # plt.xlim(-50, 50)
    plt.plot(screen_x, intensity_norm, label='Ideal Point Sources', alpha=0.7)

def simulate_realistic_double_slit(N=10, w=0.05, d=0.5, wavelength=0.0005, D=2000, W=50, points=2000, filename=None):
    k = 2*np.pi/wavelength
    screen_x = np.linspace(-W/2, W/2, points)
    
    if N > 1:
        slit1_sources = np.linspace(d/2 - w/2, d/2 + w/2, N)
        slit2_sources = np.linspace(-d/2 - w/2, -d/2 + w/2, N)
    else:
        slit1_sources = [d/2]
        slit2_sources = [-d/2]
        
    all_sources = np.concatenate([slit1_sources, slit2_sources])
    num_total = len(all_sources)
    
    intensity = np.zeros(points)
    for i, x in enumerate(screen_x):
        r_center = np.sqrt(D**2 + x**2)
        distances = [np.sqrt(D**2 + (x - sx)**2) for sx in all_sources]
        
        term_sum = 0
        for idx1 in range(num_total - 1):
            for idx2 in range(idx1 + 1, num_total):
                term_sum += np.cos(k*(distances[idx1] - distances[idx2]))
        
        intensity[i] = (num_total/2 + term_sum) / r_center**2

    # Point source model
    intensity_point = np.zeros(points)
    x1, x2 = d/2, -d/2
    for i, x in enumerate(screen_x):
        r_center = np.sqrt(D**2 + x**2)
        r1 = np.sqrt(D**2 + (x-x1)**2)
        r2 = np.sqrt(D**2 + (x-x2)**2)
        intensity_point[i] = (1 + np.cos(k*(r1-r2)))/r_center**2

    # Normalize both so central peak is 1
    intensity /= np.max(intensity)
    intensity_point /= np.max(intensity_point)

    plt.figure(figsize=(12,6))
    simulate_doubleslit()
    plt.plot(screen_x, intensity, label='Realistic Slits (N=10, w=0.05)', lw=4)
    # plt.plot(screen_x, intensity_point, '--', label='Ideal Point Sources', alpha=0.7)
    plt.xlabel('x')
    plt.ylabel('intensity (normalized)')
    plt.title(f'Double Slit Realistic: $\lambda$={wavelength}mm, d={d}mm, w={w}mm, D={D}mm, w={w}mm, N={N}')
    plt.legend()
    if filename:
        plt.savefig(filename)
        plt.close()

if __name__ == "__main__":
    os.makedirs('report/figures', exist_ok=True)
    simulate_realistic_double_slit(filename='report/figures/p4_comparison.png')
