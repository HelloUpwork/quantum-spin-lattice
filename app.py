from lattice import HoneycombLattice
from spin import Spin
from hamiltonian import Hamiltonian
from simulation import Simulation
from plotter import Plotter
from partition import ThermalProperties

import numpy as np
import pickle
class App:
    def __init__(self):
        #Todo: Create a SimulationConfiguration class
        self.rows = None
        self.cols = None
        self.j1 = None
        self.j2 = None
        self.simulation = None
        self.correlations = None
        self.ground_state_energy = None

    def set_lattice_parameters(self, rows, cols):
        self.rows = rows
        self.cols = cols

    def set_action_parameters(self, j1, j2):
        self.j1 = j1
        self.j2 = j2

    def run_simulation(self):
        if None in [self.rows, self.cols, self.j1, self.j2]:
            raise NameError("Must define rows, cols, j1, and j2")
        lattice = HoneycombLattice(self.rows, self.cols)
        self.simulation = Simulation(lattice, self.j1, self.j2)
        eigenvalues, eigenvectors = self.simulation.run()
        self.ground_state_energy = eigenvalues.min()
        
        tp = ThermalProperties(eigenvalues)

        # print(tp.calculate_partition_function(300))
        print(tp.average_energy(300))
        print(tp.heat_capacity(3000))
        print(eigenvalues.min())
        return eigenvalues, eigenvectors

    def sweep(self, num_iterations):
        N = num_iterations
        ground_states = np.zeros((N+1, N+1))
        results = {}
        for j1_idx in range(0, N+1):
            for j2_idx in range(0, N+1):
                j1 = -1.0 + j1_idx*(2/N)
                j2 = -1.0 + j2_idx*(2/N)
                self.set_action_parameters(j1, j2)
                eigenvectors, eigenvalues = self.run_simulation()
                ground_state = eigenvalues.min()
                ground_states[j1_idx][j2_idx] = ground_state
                results[(j1_idx, j2_idx)] = (eigenvalues, eigenvectors)
                print(f"For J1={j1}, J2={j2}:\tGround State Energy = {ground_state}")

        filename = 'ground_states.pkl'
        with open(filename, 'wb') as file:
            pickle.dump(ground_states, file)

        filename = 'simulation_results.pkl'
        with open(filename, 'wb') as file:
            pickle.dump(results, file)


    def plot_correlations(self):
        if self.correlations == None:
            self.correlations = self.simulation.compute_correlations()

        Plotter.correlation(self.correlations)
    
    def get_ground_state_energy(self):
        return self.ground_state_energy