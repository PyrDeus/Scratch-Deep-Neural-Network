
import random
import sys
import pandas as pd

from agent import Agent
from tetris import Tetris


import time

#TODO Still to end

def main(render=True):
    # Create canvas to replicate
    canvas = Canvas()
    level = canvas.ask_level() #pandas

    sampler = Sampler(level)
    # Ration of datasets: train = 0.8 * 0.8 = 0.64, val = 0.8 * 0.2 = 0.16, test = 0.2
    train_data, val_data, test_data = sampler.create_datas(number_samples=500, train_test_ratio=0.8, validation_ratio=0.2)

    # Initialize the agent
    agent = Agent(input_size=4)
    agent.ask_weights()

    agent.learn(canvas)

    # Training loop
    epochs = 2
    for epoch in range(epochs):
        print("\nStart of epoch %d" % (epoch,))
        start_time = time.time()

        # Iterate over the batches of the dataset.
        for step, (x_batch_train, y_batch_train) in enumerate(train_data):
            with tf.GradientTape() as tape:
                logits = model(x_batch_train, training=True)
                loss_value = loss_fn(y_batch_train, logits)
            grads = tape.gradient(loss_value, model.trainable_weights)
            optimizer.apply_gradients(zip(grads, model.trainable_weights))

            # Update training metric.
            train_acc_metric.update_state(y_batch_train, logits)

            # Log every 200 batches.
            if step % 200 == 0:
                print(
                    "Training loss (for one batch) at step %d: %.4f"
                    % (step, float(loss_value))
                )
                print("Seen so far: %d samples" % ((step + 1) * batch_size))

        # Display metrics at the end of each epoch.
        train_acc = train_acc_metric.result()
        print("Training acc over epoch: %.4f" % (float(train_acc),))

        # Reset training metrics at the end of each epoch
        train_acc_metric.reset_states()

        # Run a validation loop at the end of each epoch.
        for x_batch_val, y_batch_val in val_dataset:
            val_logits = model(x_batch_val, training=False)
            # Update val metrics
            val_acc_metric.update_state(y_batch_val, val_logits)
        val_acc = val_acc_metric.result()
        val_acc_metric.reset_states()
        print("Validation acc: %.4f" % (float(val_acc),))
        print("Time taken: %.2fs" % (time.time() - start_time))


if __name__ == "__main__":
    if len(sys.argv) >= 2:
        level = sys.argv[1]
        main(render=False)
    else:
        main()




