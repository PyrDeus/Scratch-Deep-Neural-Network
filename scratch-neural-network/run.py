
import random
import sys
import pandas as pd
import numpy as np
import time
from pathlib import Path

from level import Level
from agent import Agent

from utils import askLevelFile, askWeightFile

import matplotlib #TODO requirements ?
import matplotlib.pyplot as plt #TODO requirements ?


def main(render=True):

    # Create canvas and layout to replicate
    level = Level(edition_mode=False, render=False)
    # lvl_file = askLevelFile()
    lvl_file = Path("../levels/lvl_1.csv")
    level.loadLayout(lvl_file)

    # Ration of datasets: train = 0.8 * 0.8 = 0.64, val = 0.8 * 0.2 = 0.16, test = 0.2
    train_data, val_data, test_data = level.createDatas(number_samples=1500, train_test_ratio=0.8, train_validation_ratio=0.2)


    # Initialize the agent
    agent = Agent(learning_rate=0.01)

    # weights_file = askWeightFile()
    weights_file = None
    if not weights_file is None:
        agent.loadWeights()

    train_data = pd.concat([train_data, val_data], ignore_index=True)

    x_train = train_data[['x', 'y']].to_numpy()
    y_train = train_data[['color', 'shape']].to_dict(orient='list')
    y_train['color'] = np.array(y_train['color'], dtype=int)
    y_train['shape'] = np.array(y_train['shape'], dtype=int)

    agent.plot_model()
    agent.fit(x_train, y_train, num_epochs=300, batch_size=256)

    matplotlib.use('MacOSX')  # MacOSX
    agent.plotLearning()

    # # Training loop
    # epochs = 2
    # for epoch in range(epochs):
    #     print("\nStart of epoch %d" % (epoch,))
    #     start_time = time.time()
    #
    #     # Iterate over the batches of the dataset.
    #     for step, (x_batch_train, y_batch_train) in enumerate(train_data):
    #         with tf.GradientTape() as tape:
    #             logits = model(x_batch_train, training=True)
    #             loss_value = loss_fn(y_batch_train, logits)
    #         grads = tape.gradient(loss_value, model.trainable_weights)
    #         optimizer.apply_gradients(zip(grads, model.trainable_weights))
    #
    #         # Update training metric.
    #         train_acc_metric.update_state(y_batch_train, logits)
    #
    #         # Log every 200 batches.
    #         if step % 200 == 0:
    #             print(
    #                 "Training loss (for one batch) at step %d: %.4f"
    #                 % (step, float(loss_value))
    #             )
    #             print("Seen so far: %d samples" % ((step + 1) * batch_size))
    #
    #     # Display metrics at the end of each epoch.
    #     train_acc = train_acc_metric.result()
    #     print("Training acc over epoch: %.4f" % (float(train_acc),))
    #
    #     # Reset training metrics at the end of each epoch
    #     train_acc_metric.reset_states()
    #
    #     # Run a validation loop at the end of each epoch.
    #     for x_batch_val, y_batch_val in val_dataset:
    #         val_logits = model(x_batch_val, training=False)
    #         # Update val metrics
    #         val_acc_metric.update_state(y_batch_val, val_logits)
    #     val_acc = val_acc_metric.result()
    #     val_acc_metric.reset_states()
    #     print("Validation acc: %.4f" % (float(val_acc),))
    #     print("Time taken: %.2fs" % (time.time() - start_time))

    level.end()

if __name__ == "__main__":
    if len(sys.argv) >= 2:
        level = sys.argv[1]
        main(render=False)
    else:
        main()




