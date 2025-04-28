#TODO

from machine_learning import *
from keras.models import Sequential
from keras.layers import Dense
import os
import pandas as pd
import numpy as np
import networkx as nx

import matplotlib.pyplot as plt

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers



class ColorAgent:
    """
    Deep-learning agent.
    It interacts with the Canvas environment to understand its structure.

    It is capable of training and prediction based on the previous training.
    """
    def __init__(self, input_size=2, output_size = 6, depth = 3, gamma=0.95, loss_fct="mse",
                 opt_fct="adam", metrics=None):
        self.opt_fct = opt_fct
        self.loss_fct = loss_fct

        self.gamma = gamma

        self.output_size = output_size
        self.input_size = input_size

        hidden_units = [32, 32]
        learning_rate = 0.01
        dropout_rate = 0.5
        num_epochs = 300
        batch_size = 256

        if depth < 2:
            raise Exception("Depth must be at least 2")

        # self.network = NeuralNetwork()
        # self.network.add( Layer(input_size, activation_function='relu') )
        # self.network.extend( [ Layer(5, activation_function='relu') for _ in range(depth-2) ] )
        # self.network.add( Layer(output_size, activation_function='relu') )

        self.create_model()
        # self.model = Sequential()
        # self.model.add(Dense(64, activation="relu", input_shape=(input_size,)))
        # self.model.add(Dense(64, activation="relu"))
        # self.model.add(Dense(32, activation="relu"))
        # self.model.add(Dense(1, activation="linear"))
        # self.model.compile(optimizer=self.opt_fct, loss=self.loss_fct, metrics=self.metrics)


    def learn(self, canvas):
        model.compile(
            optimizer=keras.optimizers.Adam(learning_rate),
            loss=keras.losses.SparseCategoricalCrossentropy(from_logits=True),
            metrics=[keras.metrics.SparseCategoricalAccuracy(name="acc")],
        )
        # Create an early stopping callback.
        early_stopping = keras.callbacks.EarlyStopping(
            monitor="val_acc", patience=50, restore_best_weights=True
        )
        # Fit the model.
        history = model.fit(
            x=x_train,
            y=y_train,
            epochs=num_epochs,
            batch_size=batch_size,
            validation_split=0.15,
            callbacks=[early_stopping],
        )
        return history

    def create_model(self, hidden_units, num_classes, dropout_rate=0.2):
        inputs = layers.Input(shape=(num_features,), name="input_features")
        x = create_forward_network(hidden_units, dropout_rate, name=f"ffn_block1")(inputs)
        for block_idx in range(4):
            # Create an FFN block.
            x1 = create_forward_network(hidden_units, dropout_rate, name=f"ffn_block{block_idx + 2}")(x)
            # Add skip connection.
            x = layers.Add(name=f"skip_connection{block_idx + 2}")([x, x1])
        # Compute logits.
        logits = layers.Dense(num_classes, name="logits")(x)
        # Create the model.
        return keras.Model(inputs=inputs, outputs=logits, name="baseline")

    def create_forward_network(self, hidden_units, dropout_rate, name=None):
        fnn_layers = []

        for units in hidden_units:
            fnn_layers.append(layers.BatchNormalization())
            fnn_layers.append(layers.Dropout(dropout_rate))
            fnn_layers.append(layers.Dense(units, activation=tf.nn.gelu))

        return keras.Sequential(fnn_layers, name=name)

    def plot_learning(self, history):
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5))

        ax1.plot(history.history["loss"])
        ax1.plot(history.history["val_loss"])
        ax1.legend(["train", "test"], loc="upper right")
        ax1.set_xlabel("Epochs")
        ax1.set_ylabel("Loss")

        ax2.plot(history.history["acc"])
        ax2.plot(history.history["val_acc"])
        ax2.legend(["train", "test"], loc="upper right")
        ax2.set_xlabel("Epochs")
        ax2.set_ylabel("Accuracy")
        plt.show()

    def act_train(self, states):
        """
        This function returns the best of multiple states or a random one. A random state is returned if a random
        percentage is less than the current epsilon
        :param states: next possible states
        :return: the best state or a random state
        """
        # select a random state with a random probability
        if random.uniform(0, 1) < self.epsilon:
            return random.choice(states)

        best_score = None
        best_state = None
        # compute the Q-value for each of the next state and select the best
        scores = self._predict_scores([state for action, state in states])
        for i, (action, state) in enumerate(states):
            score = scores[i]
            if not best_score or score > best_score:
                best_score = score
                best_state = (action, state)

        return best_state

    def act_best(self, states):
        """
        Same function than act_train, however, no random states are chosen only the best one.
        :param states: next possible states
        :return: the best state
        """
        best_score = None
        best_state = None
        # compute the Q-value for each of the next state and select the best
        scores = self._predict_scores([state for action, state in states])
        for i, (action, state) in enumerate(states):
            score = scores[i]
            if not best_score or score > best_score:
                best_score = score
                best_state = (action, state)

        return best_state

    def _predict_scores(self, states):
        """
        Return the score for a list of states
        :param states: input list of states
        :return: list of q-values for each state
        """
        input = np.array(states)
        predictions = self.model.predict(input, verbose=0) # verbose = 0 to avoid progress bar
        return [prediction[0] for prediction in predictions]

    def fill_memory(self, previous_state, next_state, reward, done):
        """
        Fill the buffer with previous experiences
        :param previous_state:original state
        :param next_state:state chosen by the network
        :param reward:reward received
        :param done:boolean value to signify whether the end of an episode is reached
        """
        self.memory.append((previous_state, next_state, reward, done))

    def save(self, path: str):
        """
        save the weights of the network
        :param path: filepath where weights are saved
        """
        self.model.save_weights(path)

    def load(self, path: str):
        """
        load the weights of the network
        :param path: filepath where weights are saved
        """
        self.model.load_weights(path)

    def training_montage(self, batch_size=64, epochs=1):
        """
        Train the model and adapt its weights using the recent experiences
        :param batch_size: Number of samples used for the training
        :param epochs: number of iterations of the backpropagation
        """
        if len(self.memory) < batch_size:
            return
        # Randomly select a batch of experiences
        experiences = random.sample(self.memory, batch_size)

        # compute the target for the neural network
        next_states = [experience[1] for experience in experiences]
        scores = self._predict_scores(next_states)
        dataset = []
        target = []
        for i in range(batch_size):
            previous_state, _, reward, done = experiences[i]
            if not done:
                next_q = self.gamma * scores[i] + reward
            else:
                next_q = reward
            dataset.append(previous_state)
            target.append(next_q)
        self.model.fit(dataset, target, batch_size, epochs, verbose=0)  # train the model
        self.epsilon = max(self.epsilon * self.decay, self.epsilon_min)  # explore less
