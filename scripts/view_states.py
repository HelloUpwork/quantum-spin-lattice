# import matplotlib.pyplot as plt
# import numpy as np
# import pickle

# def load_results(filename):
#     with open(filename, 'rb') as file:
#         data = pickle.load(file)
#     return data

# def plot_eigenvectors(eigenvectors, lattice_shape):
#     plt.figure(figsize=(8, 8))
#     for i, vec in enumerate(eigenvectors.T):  # Transpose to iterate over eigenvectors
#         plt.subplot(4, 4, i+1)  # Adjust grid size depending on how many you want to display
#         plt.imshow(vec.reshape(lattice_shape), cmap='viridis')
#         plt.title(f'Eigenvector {i+1}')
#         plt.colorbar()
#     plt.tight_layout()
#     plt.show()

# def plot_ground_state_distribution(eigenvectors):
#     ground_state = eigenvectors[:, 0]

#     probabilities = np.abs(ground_state)**2
#     plt.figure(figsize=(10, 6))
#     plt.stem(probabilities)
#     plt.title('Probability Distribution of the Ground State')
#     plt.xlabel('Configuration Index')
#     plt.ylabel('Probability')
#     plt.show()
# def plot_eigenvalues(eigenvalues):
#     plt.figure()
#     plt.stem(eigenvalues)
#     plt.title('Eigenvalues')
#     plt.xlabel('Index')
#     plt.ylabel('Eigenvalue')
#     plt.show()

# # Example usage
# filename = 'output/simulation_results.pkl'
# results = load_results(filename)

# # Assuming you are interested in a specific (j1, j2) value
# j1, j2 = 32, 33  # Example values
# eigenvectors, eigenvalues = results[(j1, j2)]
# plot_ground_state_distribution(eigenvectors)


# # print(eigenvectors)
# # plot_eigenvalues(eigenvalues)  # Plot the first 16 eigenvalues
# # plot_eigenvectors(eigenvectors[:, :16], (16, 16))  # Assuming the lattice shape fits the reshaping

import math
import matplotlib.pyplot as plt
import numpy as np
import pickle

def load_results(filename):
    with open(filename, 'rb') as file:
        data = pickle.load(file)
    return data

def plot_eigenvectors(eigenvectors, lattice_shape):
    plt.figure(figsize=(8, 8))
    num_vecs = eigenvectors.shape[1]
    num_plots = min(16, num_vecs)  # Ensure we don't try to plot more than we have or more than 16
    for i in range(num_plots):
        plt.subplot(4, 4, i+1)  # Create a 4x4 grid
        plt.imshow(eigenvectors[:, i].reshape(lattice_shape), cmap='viridis')
        plt.title(f'Eigenvector {i+1}')
        plt.colorbar()
    plt.tight_layout()
    plt.show()

def plot_ground_state_distribution(eigenvectors):
    ground_state = eigenvectors[:, 0]
    probabilities = np.abs(ground_state)**2
    plt.figure(figsize=(10, 6))
    plt.stem(probabilities)
    plt.title('Probability Distribution of the Ground State')
    plt.xlabel('Configuration Index')
    plt.ylabel('Probability')
    plt.show()

def plot_eigenvalues(eigenvalues):
    plt.figure()
    plt.stem(eigenvalues)
    plt.title('Eigenvalues')
    plt.xlabel('Index')
    plt.ylabel('Eigenvalue')
    plt.show()

def main():
    filename = 'output/simulation_results.pkl'
    results = load_results(filename)
    
    print("Enter the j1 and j2 values:")
    j1 = float(input("j1: "))

    if j1 < -1.0 or j1 > 1.0:
        raise ValueError("J1 must be between -1.0 and 1.0 inclusive.")
    j1_idx = int(math.floor((j1 + 1)*32))

    j2 = float(input("j2: "))
    if j2 < -1.0 or j2 > 1.0:
        raise ValueError("J2 must be between -1.0 and 1.0 inclusive.")
    j2_idx = int(math.floor((j2 + 1)*32))
    print(j2_idx)
    if (j1_idx, j2_idx) in results:
        print(j2_idx)
        eigenvectors, eigenvalues = results[(j1_idx, j2_idx)]
        
        print("Select an option to plot:")
        print("1. Eigenvalues")
        print("2. Ground State Distribution")
        print("3. Eigenvectors")
        option = input("Option (1-3): ")
        
        if option == '1':
            plot_eigenvalues(eigenvalues)
        elif option == '2':
            plot_ground_state_distribution(eigenvectors)
        elif option == '3':
            lattice_shape = (int(np.sqrt(len(eigenvectors))), int(np.sqrt(len(eigenvectors))))
            plot_eigenvectors(eigenvectors, lattice_shape)
        else:
            print("Invalid option selected.")
    else:
        print(f"No results available for j1={j1}, j2={j2}")

if __name__ == "__main__":
    main()