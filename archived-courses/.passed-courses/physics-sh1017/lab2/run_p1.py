import numpy as np
import matplotlib.pyplot as plt
import os

def simulate_interference(separation, num_sources=2, filename=None):
    wavelength = 5.0
    k = 2*np.pi/wavelength
    side = 100.0 # sidelength
    points = 500 # number of grid points along each side
    spacing = side/points 

    # positions of wave sources
    sources = []
    if num_sources == 2:
        sources.append((side/2 + separation/2, side/2))
        sources.append((side/2 - separation/2, side/2))
    elif num_sources == 3:
        sources.append((side/2 + separation/2, side/2))
        sources.append((side/2, side/2))
        sources.append((side/2 - separation/2, side/2))

    # array to store amplitude
    xi = np.zeros([points,points], float)

    # calculate amplitudes (using broadcasting for speed)
    x = np.linspace(0, side, points)
    y = np.linspace(0, side, points)
    X, Y = np.meshgrid(x, y)

    for sx, sy in sources:
        r = np.sqrt((X-sx)**2 + (Y-sy)**2)
        xi += np.sin(k*r)

    # plot
    plt.figure(figsize=(8,6))
    plt.imshow(xi, origin='lower', extent=[-side/2, side/2, -side/2, side/2])
    plt.colorbar(label='Amplitude')
    plt.title(f'Interference Pattern: d={separation}, sources={num_sources}')
    plt.xlabel('x')
    plt.ylabel('y')
    if filename:
        plt.savefig(filename)
        plt.close()
    else:
        plt.show()

if __name__ == "__main__":
    os.makedirs('report/figures', exist_ok=True)
    # Test different distances d
    simulate_interference(separation=5.0, num_sources=2, filename='report/figures/p1_d10.png')
    simulate_interference(separation=25.0, num_sources=2, filename='report/figures/p1_d20.png')
    simulate_interference(separation=50.0, num_sources=2, filename='report/figures/p1_d40.png')
    
    # Add a third source
    simulate_interference(separation=25.0, num_sources=3, filename='report/figures/p1_3sources.png')
