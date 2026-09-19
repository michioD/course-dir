"""
Recreate the plots in lab3-example-report.pdf:
  - Figure 2: infinite square well eigenstates n=1..4
  - Figures 4-7: first four anharmonic-potential eigenstates

The plotting style and labels are chosen to match the example report as closely
as possible.  The numerics are intentionally simple, matching the spirit of the
provided eigenstates.py Verlet/shooting lab code.

Run:
    python recreate_lab3_fig2_fig4_to_fig7.py

This writes:
    fig2_infinite_box.png
    fig4_anharmonic_state_1.png
    fig5_anharmonic_state_2.png
    fig6_anharmonic_state_3.png
    fig7_anharmonic_state_4.png
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.linalg import eigh_tridiagonal


# ---------------------------------------------------------------------
# Figure 2: report-like infinite-box plot
# ---------------------------------------------------------------------
def make_fig2():
    """
    The example report's Fig. 2 is visually consistent with sine eigenstates
    scaled by about 0.30/n.  Its reported energies are exactly proportional to
    n^2 with E_1 ~= 5.428, i.e. about 0.55*pi^2, not the exact 0.5*pi^2.

    For the physically exact infinite well with L=1, replace 0.55 by 0.5.
    """
    x = np.linspace(0.0, 1.0, 2000)

    plt.figure(figsize=(7, 5))
    for n in range(1, 5):
        E = 0.55 * np.pi**2 * n**2       # matches the example-report labels
        # E = 0.5 * np.pi**2 * n**2       # matches the example-report labels
        psi = (0.30 / n) * np.sin(n * np.pi * x)
        plt.plot(x, psi, label=f"n={n}, $E_n$={E:.2f}")

    plt.axhline(0, color="y", lw=1)
    plt.axvline(0, color="y", linestyle=":", lw=1.5)
    plt.axvline(1, color="y", linestyle=":", lw=1.5)
    plt.title("Eigenstates for n=1,2,3,4 and their corresponding eigenvalue energies")
    plt.xlabel("x")
    plt.ylabel(r"$\psi$")
    plt.xlim(-0.05, 1.05)
    plt.ylim(-0.33, 0.45)
    plt.legend(loc="upper right", fontsize=8)
    plt.tight_layout()
    plt.savefig("fig2_infinite_box.png", dpi=300)
    plt.close()


# ---------------------------------------------------------------------
# Figures 4-7: anharmonic oscillator eigenstates
# ---------------------------------------------------------------------
def anharmonic_potential(x):
    # Lab instruction: V(x)=x^2/2 + x^4/2.
    return 0.5 * x**2 + 0.5 * x**4


def solve_anharmonic_dirichlet(xmax=4.0, ngrid=2000, nstates=4):
    """
    Finite-difference Hamiltonian for
        H = -1/2 d^2/dx^2 + V(x)
    on x in [0, xmax] with psi(0)=psi(xmax)=0.

    This gives the same kind of one-sided eigenstate plots as the report.
    """
    dx = xmax / (ngrid + 1)
    x = dx * np.arange(1, ngrid + 1)
    V = anharmonic_potential(x)

    # Central difference:
    # -1/2 psi'' -> diagonal 1/dx^2, off-diagonal -1/(2 dx^2)
    diag = 1.0 / dx**2 + V
    offdiag = -0.5 / dx**2 * np.ones(ngrid - 1)

    energies, states = eigh_tridiagonal(
        diag,
        offdiag,
        select="i",
        select_range=(0, nstates - 1),
    )

    # Add the boundary points back for plotting.
    x_full = np.concatenate(([0.0], x, [xmax]))
    states_full = []
    for k in range(nstates):
        psi = np.concatenate(([0.0], states[:, k], [0.0]))
        psi = psi / np.max(np.abs(psi))

        # Choose signs to resemble the example-report figures.
        if k in (1, 3):
            psi = -psi
        states_full.append(psi)

    return x_full, energies, states_full


def make_fig4_to_fig7():
    x, energies, states = solve_anharmonic_dirichlet()

    # The report labels show these values.  The numerical solver above, using
    # the lab's V=x^2/2+x^4/2, gives close but not identical values because the
    # report appears to mix/round conventions. Set this to False to label with
    # the solver's actual finite-difference eigenvalues.
    use_report_energy_labels = True
    report_E = [2.223800, 6.358469, 11.303362, 16.840037]

    captions = ["First", "Second", "Third", "Fourth"]
    for k, psi in enumerate(states):
        E_label = report_E[k] if use_report_energy_labels else energies[k]

        plt.figure(figsize=(7, 5))
        plt.plot(x, psi, color="blue", lw=1.3,
                 label=f"Eigenstate {k+1} (E={E_label:.6f})")
        plt.title(f"Eigenstate {k+1} of the Anharmonic Potential")
        plt.xlabel("x")
        plt.ylabel(r"$\psi(x)$")
        plt.xlim(0.0, 4.0)
        plt.ylim(-1.05, 1.30)
        plt.grid(True, alpha=0.5)
        plt.legend(loc="upper right", fontsize=8)
        plt.tight_layout()
        plt.savefig(f"fig{k+4}_anharmonic_state_{k+1}.png", dpi=300)
        plt.close()

    print("Anharmonic finite-difference energies from V=x^2/2+x^4/2:")
    for k, E in enumerate(energies, start=1):
        print(f"  state {k}: E = {E:.6f}")


# ---------------------------------------------------------------------
# Optional: Verlet shooting function close to eigenstates.py
# ---------------------------------------------------------------------
def verlet_shoot(E, V, xmax=1.0, N=10000, psi0=0.0, dpsi0=1.0):
    """
    Direct adaptation of the provided lab Verlet loop.  Returns x, psi, psi_end.
    Useful if you want to replace the finite-difference anharmonic solver by a
    shooting/bisection loop.
    """
    dx = xmax / N
    dx2 = dx**2
    x = 0.0
    psi = psi0
    dpsi = dpsi0
    x_tab = [x]
    psi_tab = [psi]

    for _ in range(N):
        d2psi = 2.0 * (V(x) - E) * psi
        d2psinew = 2.0 * (V(x + dx) - E) * psi
        psi += dpsi * dx + 0.5 * d2psi * dx2
        dpsi += 0.5 * (d2psi + d2psinew) * dx
        x += dx
        x_tab.append(x)
        psi_tab.append(psi)

    return np.array(x_tab), np.array(psi_tab), psi


if __name__ == "__main__":
    make_fig2()
    make_fig4_to_fig7()

