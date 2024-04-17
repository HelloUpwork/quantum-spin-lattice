import numpy as np

class Spin:
    """Class to handle spin operators."""
    def __init__(self):
        self.Sx = 0.5 * np.array([[0, 1], [1, 0]], dtype=complex)
        self.Sy = 0.5 * np.array([[0, -1j], [1j, 0]], dtype=complex)
        self.Sz = 0.5 * np.array([[1, 0], [0, -1]], dtype=complex)