import numpy as np
from abc import ABC, abstractmethod

class Lattice(ABC):
    """Abstract base class for lattice geometries."""
    def __init__(self, size):
        self.size = size
        self.edges = []
        self.next_nearest = []

    @abstractmethod
    def build_edges(self):
        """Method to build edges based on lattice geometry."""
        pass

class HoneycombLattice(Lattice):
    """Honeycomb lattice generator that dynamically calculates next-nearest neighbors."""
    def __init__(self, rows, cols):  # rows and cols define the number of hexagons in each dimension
        super().__init__((rows, cols))
        self.build_edges()

    def build_edges(self):
        rows, cols = self.size
        self.edges = []

        # Build nearest neighbor edges
        for row in range(rows):
            for col in range(cols):
                # Each cell has two parts, A and B
                A = 2 * (row * cols + col)
                B = A + 1
                
                # Horizontal connection within the cell
                self.edges.append((A, B))
                
                # Connections to adjacent cells
                if col < cols - 1:  # Connection to the right cell
                    self.edges.append((B, A + 2))
                if row < rows - 1:  # Connections to cells below
                    if col < cols - 1:
                        self.edges.append((B, A + 2 * cols + 2))  # Diagonal down-right
                    self.edges.append((B, A + 2 * cols))  # Vertical down-left

    def build_next_nearest_neighbors(self):
        """Dynamically build next-nearest neighbor relations based on the nearest neighbors."""
        # self.next_nearest = np.zeros(self.size*self.size)
        self.next_nearest = {}
        neighbor_map = {i: [] for i in range(2 * self.size[0] * self.size[1])}
        
        for i, j in self.edges:
            neighbor_map[i].append(j)
            neighbor_map[j].append(i)
        
        for k, neighbors in neighbor_map.items():
            # Find unique next-nearest neighbors by exploring neighbors of neighbors
            nnn_set = set()
            for n in neighbors:
                nnn_set.update(neighbor_map[n])
            # Remove the direct neighbors and the node itself
            nnn_set.difference_update(neighbors)
            nnn_set.discard(k)
            self.next_nearest[k] = list(nnn_set)
            # self.next_nearest.extend([(k, nnn) for nnn in nnn_set])

    def next_nearest_neighbors(self, i):
        """Retrieve next-nearest neighbors for complex interactions, if applicable."""
        if not self.next_nearest:  # Build next-nearest if not already done
            self.build_next_nearest_neighbors()
        return self.next_nearest[i]
        # return [j for j, k in self.next_nearest if i == j] + [k for j, k in self.next_nearest if i == k]


# Usage example for a small honeycomb lattice
honeycomb = HoneycombLattice(2, 2)  # Creates a lattice with 2x2 hexagons
print("Edges:", honeycomb.edges)