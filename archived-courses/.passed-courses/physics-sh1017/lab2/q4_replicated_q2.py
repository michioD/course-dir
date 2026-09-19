import numpy as np
import matplotlib.pyplot as plt
import os

def simulate_doubleslit(wavelength, d, D, W=20, points=1000, filename=None):
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

    plt.figure(figsize=(10,4))
    plt.plot(screen_x, intensity_norm)
    plt.xlabel('x (mm)')
    plt.ylabel('Normalized Intensity')
    plt.title(f'Double Slit: $\lambda$={wavelength} mm, d={d} mm, D={D} mm')
    
    # Theoretical fringe spacing: delta_x = lambda * D / d
    theoretical_spacing = wavelength * D / d
    
    # Find peaks to compare
    # Simple peak finding for approximately central fringes
    center_idx = points // 2
    search_range = points // 4 # Increased search range
    peak_indices = []
    for i in range(center_idx - search_range, center_idx + search_range):
        if intensity[i] > intensity[i-1] and intensity[i] > intensity[i+1]:
            peak_indices.append(i)
    
    measured_spacing = None
    if len(peak_indices) >= 2:
        diffs = np.diff(screen_x[peak_indices])
        measured_spacing = np.mean(diffs)

    if filename:
        plt.savefig(filename)
        plt.close()
    
    return theoretical_spacing, measured_spacing

if __name__ == "__main__":
    os.makedirs('report/figures', exist_ok=True)
    
    results = []
    # Base case
    res = simulate_doubleslit(0.0005, 0.5, 2000, filename='report/figures/p2_base.png')
    results.append(("Base", 0.0005, 0.5, 2000, res))