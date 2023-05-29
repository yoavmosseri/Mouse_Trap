from .collect_data.tools.neural_network.network import Network
from .collect_data.tools.data_utils import DataUtils

class TestData:
    """
    A class for testing the performance of a neural network model on a given set of data.
    """

    def __init__(self, network: Network, limit: float) -> None:
        """
        Initializes the TestData object with a neural network model and a cost limit.

        Args:
        - network: an instance of the Network class, which is the neural network model to be tested.
        - limit: a floating-point number representing the maximum allowed cost of the model on a given set of data.
        """
        self.network = network
        self.limit = limit

    def test(self, data: list) -> bool:
        """
        Tests the performance of the neural network model on the given set of data.

        Args:
        - data: a list of input-output pairs representing the data to test the model on.

        Returns:
        - A boolean value indicating whether the average cost of the model on the data is less than or equal to the specified limit.
        """
        cost = DataUtils.get_avg_cost(self.network, data)
        print(f"Current batch cost: {cost}, limit: {self.limit}")
        return cost <= self.limit
