from .hamiltonian import Hamiltonian
from .spin import Spin

import numpy as np

class Simulation:
    # Assume classes for Spin, Lattice, and Hamiltonian are defined as previously discussed
    def __init__(self, lattice, j1, j2):
        self.lattice = lattice
        self.hamiltonian = Hamiltonian(lattice, j1, j2)

    def run(self):
        self.hamiltonian.build(num_spins=len(set(sum(self.lattice.edges, ()))))
        eigenvalues, eigenvectors = np.linalg.eigh(self.hamiltonian.H.real)
        return eigenvalues, eigenvectors

    def compute_correlations(self):
        num_spins = len(set(sum(self.lattice.edges, ())))
        self.hamiltonian.build(num_spins)
        spin = Spin()
        correlations = np.zeros((num_spins, num_spins))

        # Calculate spin-spin correlation for each pair of spins
        for i in range(num_spins):
            for j in range(num_spins):
                if i != j:
                    correlations[i, j] = self.spin_spin_correlation(i, j, spin)
        return correlations

    def spin_spin_correlation(self, i, j, spin):
        """Calculate the expectation value of Si.Sj - <Si><Sj>."""
        Sx_i = self.hamiltonian.kron_prod(len(self.lattice.edges), i, spin.Sx)
        Sy_i = self.hamiltonian.kron_prod(len(self.lattice.edges), i, spin.Sy)
        Sz_i = self.hamiltonian.kron_prod(len(self.lattice.edges), i, spin.Sz)

        Sx_j = self.hamiltonian.kron_prod(len(self.lattice.edges), j, spin.Sx)
        Sy_j = self.hamiltonian.kron_prod(len(self.lattice.edges), j, spin.Sy)
        Sz_j = self.hamiltonian.kron_prod(len(self.lattice.edges), j, spin.Sz)

        S_i_dot_S_j = np.dot(Sx_i, Sx_j) + np.dot(Sy_i, Sy_j) + np.dot(Sz_i, Sz_j)
        correlation = np.vdot(self.ground_state, S_i_dot_S_j @ self.ground_state).real
        
        # Subtract <Si><Sj>
        mean_S_i = np.vdot(self.ground_state, (Sx_i + Sy_i + Sz_i) @ self.ground_state).real
        mean_S_j = np.vdot(self.ground_state, (Sx_j + Sy_j + Sz_j) @ self.ground_state).real
        correlation -= mean_S_i * mean_S_j

        return correlation