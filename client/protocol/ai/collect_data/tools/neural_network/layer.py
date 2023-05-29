import numpy as np


class Layer:
    def __init__(self, input_len: int, output_len: int, activation, activation_deriv):
        """
        Initializes a layer of a neural network with random weights and biases.

        Args:
            input_len (int): number of input neurons for the layer
            output_len (int): number of output neurons for the layer
            activation (function): activation function to be used for the layer
            activation_deriv (function): derivative of the activation function
        """
        # between -1 and 1
        self.weights = (np.random.rand(input_len, output_len) - 0.5) * 2
        self.bias = (np.random.rand(output_len) - 0.5) * 2
        self.activation = activation
        self.activation_deriv = activation_deriv

    def __calc_derivs(self, output_array, target_array):
        """
        Calculates the derivatives of weights, biases, and inputs with respect to the cost function.

        Args:
            output_array (np.array): output of the layer after applying activation function
            target_array (np.array): target output for the layer

        Returns:
            Tuple containing the derivatives of weights, biases, and inputs with respect to the cost function.
        """
        # derivative of cost with respect to output
        cost_deriv = 2*(output_array - target_array)
        # derivative of activation function with respect to output without activation
        sigmoid_deriv = self.activation_deriv(self.output_no_activation)

        # derivative of input with respect to cost
        input_deriv = np.dot(cost_deriv*sigmoid_deriv, self.weights.T)
        # derivative of bias with respect to cost
        bias_deriv = (cost_deriv * sigmoid_deriv).flatten()
        # derivative of weights with respect to cost
        weights_deriv = np.outer(self.input, (cost_deriv*sigmoid_deriv))

        return weights_deriv, bias_deriv, input_deriv

    def __update_values(self, weights_deriv, bias_deriv, learning_rate):
        """
        Updates the weights and biases based on their derivatives.

        Args:
            weights_deriv (np.array): derivative of the weights with respect to the cost function
            bias_deriv (np.array): derivative of the bias with respect to the cost function
            learning_rate (float): learning rate for updating weights and biases
        """
        self.weights -= weights_deriv * learning_rate
        self.bias -= bias_deriv * learning_rate

    def forward_propagation(self, input_array: np.array):
        """
        Calculates the output of the layer for a given input.

        Args:
            input_array (np.array): input to the layer

        Returns:
            Output of the layer after applying the activation function.
        """
        # calculate dot product of input and weights, add bias term, and apply activation function
        self.output_no_activation = np.dot(
            input_array, self.weights) + self.bias
        return self.activation(self.output_no_activation)

    def backward_propagation(self, input_array, target_array, learning_rate):
        """
        Performs backpropagation on the layer and updates the weights and biases.

        Args:
            input_array (np.array): input to the layer
            target_array (np.array): target output for the layer
            learning_rate (float): learning rate for updating weights and biases

        Returns:
            Derivative of the input with respect to the cost function, needed for backpropagation in previous layers.
        """
        # store input for later use
        self.input = input_array
        # calculate output using forward propagation
        output_array = self.forward_propagation(self.input)

        # calculate derivatives with respect to cost
        weights_deriv, bias_deriv, input_deriv = self.__calc_derivs(
            output_array, target_array)

        # update weights and biases based on derivatives
        self.__update_values(weights_deriv, bias_deriv, learning_rate)

        # return derivative of input with respect to cost for backpropagation in previous layers
        return input_array - input_deriv
