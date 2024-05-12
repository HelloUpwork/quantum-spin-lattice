import numpy as np
import matplotlib.pyplot as plt

class PointCharge:
    def __init__(self, position, charge):
        self.position = np.array(position)
        self.charge = charge

    def potential_at(self, r):
        r_vec = np.array(r) - self.position
        distance = np.linalg.norm(r_vec)
        if distance != 0:
            return self.charge / (4 * np.pi * distance)
        else:
            return np.inf  # Singularity at the charge position

class PotentialField:
    def __init__(self, charges):
        self.charges = charges

    def compute_potential(self, x, y, z):
        X, Y, Z = np.meshgrid(x, y, z, indexing='ij')
        phi = np.zeros_like(X)
        r = np.array([X, Y, Z])
        for charge in self.charges:
            phi += charge.potential_at(r)
        return X, Y, Z, phi

# Usage
charge1 = PointCharge([0, 0, 0], 1.0)
charge2 = PointCharge([0,1,0], 1.0)
field = PotentialField([charge1, charge2])
x = np.linspace(-1, 1, 100)
y = np.linspace(-1, 1, 100)
z = np.array([0])
X, Y, Z, phi = field.compute_potential(x, y, z)

# Plotting
fig, ax = plt.subplots()
cp = ax.contourf(X[:, :, 0], Y[:, :, 0], phi[:, :, 0], 50, cmap='viridis')
fig.colorbar(cp)
ax.set_title('Potential Contour of a Point Charge')
ax.set_xlabel('X')
ax.set_ylabel('Y')
plt.show()
