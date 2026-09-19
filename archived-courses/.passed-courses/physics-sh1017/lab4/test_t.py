import numpy as np
from q3 import run_simulation_q3
T = run_simulation_q3(V_type='slanted', V0=1.0, E=0.5)
print("T =", T)
print("ln T =", np.log(T))
