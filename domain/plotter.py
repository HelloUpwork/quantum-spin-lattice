import matplotlib.pyplot as plt

class Plotter:
    @staticmethod
    def correlation(correlations):
        plt.imshow(correlations, cmap='viridis')
        plt.colorbar()
        plt.title('Spin-Spin Correlation Matrix')
        plt.show()