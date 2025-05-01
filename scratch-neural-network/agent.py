

from keras import Sequential, Input, Model
# from keras import layers
from keras.layers import Dense, BatchNormalization, BatchNormalization, Dropout, Activation
from keras.losses import SparseCategoricalCrossentropy, CategoricalCrossentropy
from keras.regularizers import L1, L2, L1L2
from keras.initializers import GlorotUniform, GlorotNormal, TruncatedNormal, RandomUniform, RandomNormal
from keras.activations import relu, linear, gelu
from keras.optimizers import Adam
from keras.metrics import SparseCategoricalAccuracy, CategoricalAccuracy
from keras.callbacks import EarlyStopping
from keras.utils import plot_model

import os
import pandas as pd
import numpy as np
import networkx as nx

import matplotlib.pyplot as plt

# import tensorflow as tf
# from tensorflow import keras
# from tensorflow.keras import layers


COLOR_NB = 6
SHAPE_NB = 5

class Agent:
    """
    Deep-learning agent.
    It interacts with the Canvas environment to understand its structure.

    It is capable of training and prediction based on the previous training.
    """
    def __init__(self, learning_rate=0.01, loss_fct=SparseCategoricalCrossentropy(from_logits=True),
                 opt_fct=Adam, dropout_rate = 0.5, metrics=None):
        self.model = None
        self.history = None
        self.opt_fct = opt_fct
        self.loss_fct = loss_fct

        self.hidden_shape = [32, 32, 32]
        self.input_size = 2
        self.output_size = [5, 6]

        self.learning_rate = learning_rate
        self.dropout_rate = dropout_rate
        # self.num_epochs = 300
        # self.batch_size = 256

        # self.network = NeuralNetwork()
        # self.network.add( Layer(input_size, activation_function='relu') )
        # self.network.extend( [ Layer(5, activation_function='relu') for _ in range(depth-2) ] )
        # self.network.add( Layer(output_size, activation_function='relu') )

        self.createModel()

    def plot_model(self):
        plot_model(self.model, to_file="plot_model.png")

    def fit(self, x_train, y_train, num_epochs=300, batch_size=256, validation_split=0.2):
        # Fit the model.
        self.history = self.model.fit(
            x=x_train,
            y=y_train,
            epochs=num_epochs,
            batch_size=batch_size,
            validation_split=validation_split,
            callbacks=[
                EarlyStopping(
                    monitor="val_loss", patience=30, restore_best_weights=True, mode='min'
                )],
        )
        return self.history

    # def createModel(self): #OLD
    #     self.model = Sequential()
    #     self.model.add(Input(shape=(self.input_size,)))
    #     # self.model.add(Dense(16, activation=linear, kernel_initializer=GlorotUniform()))
    #     for neuron_nb in self.hidden_shape:
    #         self.model.add(BatchNormalization())
    #         self.model.add(Dropout(self.dropout_rate))
    #         self.model.add(Dense(neuron_nb, kernel_initializer=GlorotUniform(), kernel_regularizer=L1(l1=0.01), activation=gelu))
    #     self.model.add(Dense(self.output_size, activation=linear, kernel_initializer=GlorotUniform()))
    #     self.model.compile(optimizer=self.opt_fct(learning_rate=self.learning_rate), loss=self.loss_fct,
    #         metrics=[SparseCategoricalAccuracy(name="acc")])

    def createModel(self):
        inputs = Input(shape=(self.input_size,))
        x = inputs
        for neuron_nb in self.hidden_shape:
            x = BatchNormalization()(x)
            x = Dropout(self.dropout_rate)(x)
            x = Dense(neuron_nb, kernel_initializer=GlorotUniform(), kernel_regularizer=L1(0.01), activation=gelu)(x)

        # Two output heads
        shape_output = Dense(SHAPE_NB, activation='softmax', name='shape')(x)
        color_output = Dense(COLOR_NB, activation='softmax', name='color')(x)

        self.model = Model(inputs=inputs, outputs=[shape_output, color_output])
        self.model.compile(
            optimizer=self.opt_fct(learning_rate=self.learning_rate),
            loss={
                'shape': SparseCategoricalCrossentropy(),
                'color': SparseCategoricalCrossentropy()
            },
            metrics={
                'shape': [SparseCategoricalAccuracy(name='shape_acc')],
                'color': [SparseCategoricalAccuracy(name='color_acc')]
            }
        )


    def plotLearning(self):
        fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15, 5))

        ax1.plot(self.history.history["loss"])
        ax1.plot(self.history.history["val_loss"])
        ax1.legend(["train", "val"], loc="upper right")
        ax1.set_xlabel("Epochs")
        ax1.set_ylabel("Loss")

        # print(self.history.history.keys())

        ax2.plot(self.history.history["color_color_acc"])
        ax2.plot(self.history.history["val_color_color_acc"])
        ax2.legend(["train", "val"], loc="upper right")
        ax2.set_xlabel("Epochs")
        ax2.set_ylabel("Color Accuracy")

        ax3.plot(self.history.history["shape_shape_acc"])
        ax3.plot(self.history.history["val_shape_shape_acc"])
        ax3.legend(["train", "val"], loc="upper right")
        ax3.set_xlabel("Epochs")
        ax3.set_ylabel("Shape Accuracy")
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
