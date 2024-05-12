import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

# Parameters
omega = 1.0  # Angular frequency

# Define the differential equation for the Green's function
def green_function(G, t):
    G0, G1 = G
    dGdt = [G1, -omega**2 * G0]
    return dGdt

# Time points
t = np.linspace(-10, 10, 1000)
G_init = [0, 1]  # Initial condition: G(0) = 0, dG/dt(0) = 1

# Solve the differential equation
G = odeint(green_function, G_init, t)

# Extract the Green's function (displacement as a function of time)
G_t = G[:, 0]

# Plot the Green's function
plt.figure(figsize=(8, 4))
plt.plot(t, G_t, label="Green's Function (G(t))")
plt.title("Green's Function for a Harmonic Oscillator")
plt.xlabel("Time t")
plt.ylabel("G(t)")
plt.grid(True)
plt.legend()
plt.show()
