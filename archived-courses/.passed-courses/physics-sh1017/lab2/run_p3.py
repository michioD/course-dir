import numpy as np
import matplotlib.pyplot as plt
import os

# wave parameters
wavelength = 0.0005 # mm = 5000 Ångström, green light
k = 2*np.pi/wavelength

# geometry parameters
D = 2000 # distance to detector screen
W = 100 # width of detector screen to see diffraction envelope
points = 2000 # number of pixels of detector screen
w = 0.05 # slit width

os.makedirs('report/figures', exist_ok=True)

N_values = [2, 3, 5, 10]
screen = np.linspace(-W/2, W/2, points)
r_center = np.sqrt(D**2 + screen**2)

for N in N_values:
    source_positions = np.linspace(-w/2, w/2, N)
    intensity = np.zeros(points)
    
    for i, x in enumerate(screen):
        distances = [np.sqrt(D**2 + (x - sx)**2) for sx in source_positions]
        
        term_sum = 0
        for idx1 in range(N - 1):
            for idx2 in range(idx1 + 1, N):
                term_sum += np.cos(k*(distances[idx1] - distances[idx2]))
        
        intensity[i] = (N/2 + term_sum) / r_center[i]**2

    plt.figure(figsize=(6,4))
    plt.plot(screen, intensity, color='purple')
    plt.xlabel('x (mm)')
    plt.ylabel('intensity')
    plt.title(f'Single Slit: N={N}')
    plt.tight_layout()
    plt.savefig(f'report/figures/p3_N{N}.png')
    plt.close()

w = 0.2
for N in N_values:
    source_positions = np.linspace(-w/2, w/2, N)
    intensity = np.zeros(points)
    
    for i, x in enumerate(screen):
        distances = [np.sqrt(D**2 + (x - sx)**2) for sx in source_positions]
        
        term_sum = 0
        for idx1 in range(N - 1):
            for idx2 in range(idx1 + 1, N):
                term_sum += np.cos(k*(distances[idx1] - distances[idx2]))
        
        intensity[i] = (N/2 + term_sum) / r_center[i]**2

    plt.figure(figsize=(6,4))
    plt.plot(screen, intensity, color='purple')
    plt.xlabel('x (mm)')
    plt.ylabel('intensity')
    plt.title(f'Single Slit: N={N}')
    plt.tight_layout()
    plt.savefig(f'report/figures/p3_N_diff_w{N}.png')
    plt.close()
