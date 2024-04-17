import numpy as np

class ThermalProperties:
    def __init__(self, eigenvalues):
        self.eigenvalues = eigenvalues
        self.last_computed_z = None

    def calculate_partition_function(self, temperature):
        kB = 8.617333262145e-5  # Boltzmann constant in eV/K
        beta = 1 / (kB * temperature)
        self.Z = np.sum(np.exp(-beta * self.eigenvalues))
        return self.Z
    
    def average_energy(self, temperature):
        self.recalculate_z_if_needed(temperature)
        kB = 8.617333262145e-5
        beta = 1 / (kB * temperature)
        weighted_energies = self.eigenvalues * np.exp(-beta * self.eigenvalues)
        self.average_E = np.sum(weighted_energies) / self.Z
        return self.average_E

    def heat_capacity(self, temperature):
        self.recalculate_z_if_needed(temperature)
        kB = 8.617333262145e-5
        beta = 1 / (kB * temperature)
        weighted_energies_squared = (self.eigenvalues**2) * np.exp(-beta * self.eigenvalues)
        average_E_squared = np.sum(weighted_energies_squared) / self.Z
        heat_cap = (beta**2) * (average_E_squared - self.average_E**2) * kB
        return heat_cap

    def recalculate_z_if_needed(self, temperature):
        if self.last_computed_z != temperature:
            self.calculate_partition_function(temperature)
            self.last_computed_z = temperature