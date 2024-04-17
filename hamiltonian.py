import numpy as np

from spin import Spin
class Hamiltonian:
    """Class to construct and manage the Hamiltonian of the system, including next-nearest neighbor interactions."""
    def __init__(self, lattice, J1=1.0, J2=0.1):
        self.lattice = lattice
        self.J1 = J1  # Nearest neighbor interaction strength
        self.J2 = J2  # Next-nearest neighbor interaction strength
        self.H = None

    def build(self, num_spins):
        """Build the Hamiltonian matrix with nearest and next-nearest neighbor interactions."""
        spin = Spin()
        N = num_spins
        H = np.zeros((2**N, 2**N), dtype=complex)

        # Nearest neighbor interactions
        for i, j in self.lattice.edges:
            H += self.add_interaction(N, i, j, spin, self.J1)

        # Next-nearest neighbor interactions
        for i in range(N):
            # print(i)
            for j in self.lattice.next_nearest_neighbors(i):
                # print(i, j)
                H += self.add_interaction(N, i, j, spin, self.J2)

        self.H = H

    def add_interaction(self, N, i, j, spin, J):
        """Helper function to add interaction terms to the Hamiltonian."""
        result = np.zeros((2**N, 2**N), dtype=complex)
        for op1, op2 in [(spin.Sx, spin.Sx), (spin.Sy, spin.Sy), (spin.Sz, spin.Sz)]:
            result += J * (self.kron_prod(N, i, op1) @ self.kron_prod(N, j, op2))
        return result

    def kron_prod(self, N, idx, op):
        """Kronecker product of identity matrices with a Pauli matrix at position idx."""
        matrices = [np.eye(2) if k != idx else op for k in range(N)]
        result = matrices[0]
        for mat in matrices[1:]:
            result = np.kron(result, mat)
        return result