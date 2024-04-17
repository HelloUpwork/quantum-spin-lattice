import pickle
import numpy as np
import matplotlib.pyplot as plt

def load_pickle_data(filename):
    """ Load data from a pickle file. """
    with open(filename, 'rb') as file:
        data = pickle.load(file)
    return data

def plot_data_as_image(data, cmap='gray'):
    """ Plot the data as a grayscale image. """
    plt.imshow(data, cmap=cmap, interpolation='nearest')
    plt.colorbar()  # Add a colorbar to a plot
    plt.title('Grayscale Image of Simulation Results')
    plt.show()

def main():
    # Load the results from the pickle file
    filename = 'output/ground_states.pkl'
    results = load_pickle_data(filename)
    
    # Plot the results as a grayscale image
    plot_data_as_image(results)

if __name__ == '__main__':
    main()