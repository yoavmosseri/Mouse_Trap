import pickle, base64
from .layer import Layer
import numpy as np
import datetime
import os

class Network:
    """
    A class representing a feedforward neural network.

    Attributes:
    layers (list): A list of Layer objects representing the layers in the network.
    time (str): A string representing the current time in the format of "%Y-%m-%d_%H-%M-%S".

    Methods:
    __init__(self, layers_len: list, activations: list, activations_derivs: list, load=False, filename=None) -> None:
        Initializes the network by creating a list of layers based on the 'layers_len' list, which specifies the number of neurons in each layer. It also takes 'activations' and 'activations_derivs' lists, which contain activation and derivative functions for each layer. If the 'load' parameter is set to True, it reads a saved network from a file specified by the 'filename' parameter.

    calc_cost(self, input_array, target_array) -> float:
        Calculates the cost of the network for a given input and target output.

    train(self, x_train, y_train, learning_rate, cost_to_stop=0.001) -> None:
        Trains the network using the backpropagation algorithm and the specified 'learning_rate'. It continues training until the total cost falls below the 'cost_to_stop' threshold.

    predict(self, input_array) -> np.ndarray:
        Predicts the output for a given input by propagating it through the layers.

    save(self) -> None:
        Saves the network to a file in a specific directory.
    """
    def __init__(self, layers_len: list, activations: list, activations_derivs: list, load=False, filename=None) -> None:
        """
        Initializes the network by creating a list of layers based on the 'layers_len' list, which specifies the number of neurons in each layer. It also takes 'activations' and 'activations_derivs' lists, which contain activation and derivative functions for each layer. If the 'load' parameter is set to True, it reads a saved network from a file specified by the 'filename' parameter.
        
        Args:
        layers_len (list): A list of integers representing the number of neurons in each layer.
        activations (list): A list of activation functions for each layer.
        activations_derivs (list): A list of derivative functions for each layer.
        load (bool): A flag indicating whether to load a saved network from a file.
        filename (str): The name of the file to load the network from.

        Returns:
        None
        """
        if not load:
            self.layers = []
            for i in range(len(layers_len) - 1):
                layer = Layer(layers_len[i], layers_len[i+1],
                            activations[i], activations_derivs[i])
                self.layers.append(layer)
        else:
            with open(f'{os.path.dirname(os.path.abspath(__file__))}\\{filename}','r') as f:
                self.layers = pickle.loads(base64.b64decode(f.read().encode()))

        now = datetime.datetime.now()
        self.time = now.strftime("%Y-%m-%d_%H-%M-%S")       

    def calc_cost(self, input_array, target_array):
        """
        Calculates the cost of the network for a given input and target output.
        
        Args:
        input_array (np.ndarray): A numpy array representing the input to the network.
        target_array (np.ndarray): A numpy array representing the desired output from the network.

        Returns:
        A float representing the cost of the network for the given input and target output.
        """
        output = self.predict(input_array)
        return np.sum(np.square(output - (target_array)))

    def train(self, x_train, y_train, learning_rate, cost_to_stop=0.001):
        """
        Trains the network using the backpropagation algorithm and the specified 'learning_rate'. It continues training until the total cost falls below the 'cost_to_stop' threshold.

        Args:
        x_train (np.ndarray): A 2D numpy array representing the training inputs.
        y_train (np.ndarray): A 2D numpy array representing the target outputs for each training input.
        learning_rate (float): The learning rate used for training.
        cost_to_stop (float): The threshold value for the total cost of the network, below which training will stop.

        Returns:
        None
        """
        total_cost = 1
        length = len(x_train)
        times = 0

        while total_cost > cost_to_stop:
            total_cost = 0
            for i, input_array in enumerate(x_train):
                target = y_train[i]

                output = input_array
                outputs = []
                for layer in self.layers:
                    outputs.append(output)
                    output = layer.forward_propagation(output)

                for j, layer in enumerate(reversed(self.layers)):
                    target = layer.backward_propagation(
                        outputs[-j-1], target, learning_rate)

                total_cost += self.calc_cost(input_array, y_train[i])

            total_cost /= length
            learning_rate = total_cost / 1.5
            times += 1

            self.save()

            print(f"{times} times | total cost: {total_cost} | learning rate: {learning_rate}")

    def predict(self, input_array):
        """
        Predicts the output for a given input by propagating it through the layers.

        Args:
        input_array (np.ndarray): A 1D numpy array representing the input to the network.

        Returns:
        np.ndarray: A 1D numpy array representing the output of the network for the given input.
        """
        for layer in self.layers:
            input_array = layer.forward_propagation(input_array)
        return input_array

    def save(self):
        """
        Saves the network to a file in a specific directory.

        Returns:
        None
        """
        with open(f'{os.path.dirname(os.path.abspath(__file__))}\\nets\\network_{self.time}.net','w') as f:
            f.write(base64.b64encode(pickle.dumps(self.layers)).decode())
