import math
import numpy as np
import matplotlib.pyplot as plt

# Generate data
x = -math.inf
s = np.random.randint(0, 10, 20)
t = [np.random.randint(s_i, 10) for s_i in s]  # fixed shape issue
intervals = sorted(list(zip(s, t)), key=lambda x: x[0])

# Function to assign non-overlapping levels
def assign_levels(intervals):
    levels = []
    placement = []
    
    for start, end in intervals:
        placed = False
        for level_index, level in enumerate(levels):
            # Check if it overlaps with last interval in that level
            if start > level[-1][1]:
                level.append((start, end))
                placement.append((start, end, level_index))
                placed = True
                break
        
        if not placed:
            levels.append([(start, end)])
            placement.append((start, end, len(levels) - 1))
    
    return placement

placement = assign_levels(intervals)

# Plot
plt.figure(figsize=(10, 6))

for start, end, level in placement:
    plt.plot([start, end], [level, level], linewidth=6)

plt.xlabel("Time")
plt.ylabel("Level")
plt.title("Intervals Without Overlap")
plt.yticks(range(max(p[2] for p in placement) + 1))
plt.grid(True)

plt.show()
