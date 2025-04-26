

import numpy as np

def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def relu(x):
    # rectified linear unit
    return np.maximum(0, x)

def tanh(x):
    return np.tanh(x)

def softmax(x):
    exp_x = np.exp(x - np.max(x))
    return exp_x / exp_x.sum(axis=0)

def linear(x):
    return x

def sigmoid_derivative(x):
    return x * (1 - x)

def relu_derivative(x):
    return np.where(x > 0, 1, 0)

def tanh_derivative(x):
    return 1 - x**2

def softmax_derivative(output):
    s = output.reshape(-1, 1)
    return np.diagflat(s) - np.dot(s, s.T)

def linear_derivative(x):
    return 1

class Neuron:
    def __init__(self, input_size, activation_function='sigmoid'):
        self.weights = np.random.rand(input_size)
        self.bias = np.random.rand()
        self.__update_activation_function(activation_function)

    def __update_activation_function(self, function_name):
        self.activation_function = {"sigmoid":sigmoid, "relu":relu, "tanh":tanh, "softmax":softmax, "linear":linear}[function_name]

    def activate(self, x):
        return self.activation_function(x)

    def forward(self, inputs):
        z = np.dot(inputs, self.weights) + self.bias
        return self.activate(z)


class Layer:
    def __init__(self, input_size, output_size, activation_function='sigmoid'):
        self.neurons = [Neuron(input_size, activation_function) for _ in range(output_size)]

    def forward(self, inputs):
        return np.array([neuron.forward(inputs) for neuron in self.neurons])


class NeuralNetwork:
    def __init__(self, layers, learning_rate):
        self.layers = layers
        self.learning_rate = learning_rate

    def forward(self, inputs):
        for layer in self.layers:
            inputs = layer.forward(inputs)
        return inputs

    def backward(self, X, y):
        # Calculate the gradient for the last layer
        last_layer = self.layers[-1]
        error = last_layer.outputs - y
        for neuron, err in zip(last_layer.neurons, error):
            neuron.delta = err * neuron.activation_derivative(neuron.output)

        # Propagate the error backwards
        for i in range(len(self.layers) - 2, -1, -1):
            layer = self.layers[i]
            next_layer = self.layers[i + 1]
            for j, neuron in enumerate(layer.neurons):
                error = sum(n.weights[j] * n.delta for n in next_layer.neurons)
                neuron.delta = error * neuron.activation_derivative(neuron.output)

        # Update weights and biases
        for layer in self.layers:
            for neuron in layer.neurons:
                neuron.weights -= self.learning_rate * neuron.delta * neuron.inputs
                neuron.bias -= self.learning_rate * neuron.delta

    def train(self, X, y, epochs):
        for epoch in range(epochs):
            for i in range(len(X)):
                outputs = self.forward(X[i])
                loss = self.compute_loss(outputs, y[i])
                self.backward(X[i], y[i])
                print(f"Epoch {epoch+1}, Loss: {loss}")

    def compute_loss(self, outputs, target):
        return np.mean((outputs - target) ** 2)  # Mean squared error



if __name__ == "__main__":
    # Example usage:
    neuron_sigmoid = Neuron(input_size=3, activation_function='sigmoid')
    neuron_relu = Neuron(input_size=3, activation_function='relu')

    inputs = np.array([0.5, -0.2, 0.1])
    print(neuron_sigmoid.forward(inputs))
    print(neuron_relu.forward(inputs))


    # Example usage:
    layer1 = Layer(input_size=3, output_size=4, activation_function='relu')
    layer2 = Layer(input_size=4, output_size=2, activation_function='sigmoid')
    network = NeuralNetwork(layers=[layer1, layer2])

    inputs = np.array([0.5, -0.2, 0.1])
    outputs = network.forward(inputs)
    print(outputs)





