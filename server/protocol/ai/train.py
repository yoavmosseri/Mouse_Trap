from .collect_data.tools.neural_network.network import Network
from .collect_data.tools.neural_network.activations import sigmoid, sigmoid_deriv
from time import time
from .collect_data.tools.variables.constants import MIN_DATA_AMOUNT


class Train:
    """
    A class that contains methods for training a neural network.
    """

    @staticmethod
    def check_if_data_is_enough(data_len):
        """
        Check if the length of the data is greater than or equal to a minimum amount specified in MIN_DATA_AMOUNT.

        Args:
            data_len (int): The length of the data.

        Returns:
            bool: True if the length of the data is greater than or equal to MIN_DATA_AMOUNT, False otherwise.
        """
        return data_len >= MIN_DATA_AMOUNT

    @staticmethod
    def check_user_ready_for_training(data):
        """
        Check if the length of data is enough for training.

        Args:
            data (list): A list of training data.

        Returns:
            bool: True if the length of the data is greater than or equal to MIN_DATA_AMOUNT, False otherwise.
        """
        if Train.check_if_data_is_enough(len(data)):
            return True

        return False

    @staticmethod
    def create_new_network():
        """
        Create a new network object with a specified architecture and activation functions.

        Returns:
            Network: A new network object.
        """
        return Network([3, 9, 27, 81, 243, 81, 27, 9, 3], 8*[sigmoid], 8*[sigmoid_deriv])

    @staticmethod
    def trainNormal(network: Network, data_x: list, data_y: list, cost_to_stop=0.01):
        """
        Train a neural network with specified training data and a cost function.

        Args:
            network (Network): The neural network object to be trained.
            data_x (list): A list of training inputs.
            data_y (list): A list of training outputs.
            cost_to_stop (float, optional): The cost function to stop training when the cost reaches this threshold. Defaults to 0.01.

        Returns:
            Network: The trained neural network object.
        """
        print('>>>>>>>>>>>>>>>>\t\tTraining Started\t\t<<<<<<<<<<<<<<<<')
        start_time = time()
        network.train(data_x, data_y, 0.1, cost_to_stop)
        end_time = time()
        print(
            f'>>>>>>>>>>>>>>>>\tTraining Ended after {int((end_time-start_time)/60)} minutes\t\t<<<<<<<<<<<<<<<<')

        return network

    @staticmethod
    def train(network: Network, data: list, cost_to_stop=0.01):
        """
        Train a neural network with specified training data and a cost function (Auto Encoder).

        Args:
            network (Network): The neural network object to be trained.
            data (list): A list of training inputs and outputs.
            cost_to_stop (float, optional): The cost function to stop training when the cost reaches this threshold. Defaults to 0.01.

        Returns:
            Network: The trained neural network object.
        """
        return Train.trainNormal(network, data, data, cost_to_stop)
