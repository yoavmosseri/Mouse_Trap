import numpy as np
from .neural_network.network import Network
from .variables.constants import V_MIN, X_MAX, X_MIN, Y_MAX, Y_MIN, V_MAX

class DataUtils:
    """
    A class containing utility methods for data preprocessing and analysis.
    """

    @staticmethod
    def normalize_data(data: np.ndarray, max_speed: float = -1) -> np.ndarray:
        """
        Normalizes the input data between 0 and 1.

        Args:
            data: A numpy array of shape (n_samples, 3) containing the x, y, and v values for each sample.
            max_speed: A float representing the maximum speed to use for normalization of the v values.
                If set to -1 (default), the maximum v value in the data is used.

        Returns:
            A numpy array of the same shape as the input data, where the x, y, and v values are normalized between 0 and 1.
        """
        x = data[:, 0]
        x = (x - X_MIN) / (X_MAX - X_MIN)

        y = data[:, 1]
        y = (y - Y_MIN) / (Y_MAX - Y_MIN)

        v = data[:, 2]
        if max_speed == -1:
            v = (v - V_MIN) / (v.max() - V_MIN)
        else:
            v = (v - V_MIN) / (max_speed - V_MIN)

        return np.stack((x, y, v), axis=1)

    @staticmethod
    def dots_to_array(dots: list) -> np.ndarray:
        """
        Converts a list of Dot instances to a 2D numpy array.

        Args:
            dots: A list of Dot instances.

        Returns:
            A 2D numpy array of shape (n_samples, 3) containing the x, y, and v values for each Dot instance.
        """
        dot_values = [(dot.x, dot.y, dot.v) for dot in dots]
        array_2d = np.array(dot_values)
        return array_2d

    @staticmethod
    def get_avg_cost(network: Network, data: list) -> float:
        """
        Calculates the average cost of the autoencoder for the input data.

        Args:
            network: A Network instance representing the autoencoder model.
            data: A list of input data items.

        Returns:
            A float representing the average cost of the autoencoder for the input data.
        """
        cost_sum = 0

        for item in data:
            cost_sum += network.calc_cost(item, item)

        return cost_sum / len(data)

    @staticmethod
    def get_accuracy(network: Network, data: list) -> float:
        """
        Calculates the average output value of the final layer of the neural network for the input data.

        Args:
            network: A Network instance representing the neural network model.
            data: A list of input data items.

        Returns:
            A float representing the average output value of the final layer of the neural network for the input data.
        """
        prediction = 0

        for item in data:
            prediction += network.predict(item)

        return prediction / len(data)
    
    def format_new(raw_data):
        """
        Formats new user data and normalizes it.

        Args:
            raw_data (list): A list of raw data to be formatted and normalized.

        Returns:
            numpy.ndarray: The formatted and normalized data.
        """
        # Convert the raw data to an array using the DataUtils.dots_to_array() method
        raw_data = DataUtils.dots_to_array(raw_data)

        # Normalize the data using the DataUtils.normalize_data() method
        return DataUtils.normalize_data(raw_data, V_MAX)
