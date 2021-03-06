import tensorflow as tf
from tensorflow import keras
import numpy as np
import os
import math

modelLocation = "python/Model.h5"


def truncate(number, digits):
    stepper = 10.0 ** digits
    return math.trunc(stepper * number) / stepper


class Model():

    def __init__(self):
        self.data = keras.datasets.mnist
        if os.path.exists(modelLocation):
            self.model = tf.keras.models.load_model(modelLocation)
        else:
            self.MakeModel()

    def MakeModel(self):
        # TODO: Don't separate into test and train, you only want to train
        (train_images, train_labels), (test_images,
                                       test_labels) = self.data.load_data()

        train_images = train_images/255.0
        test_images = test_images/255.0

        self.model = keras.Sequential([
            keras.layers.Flatten(input_shape=(28, 28)),
            keras.layers.Dense(128, activation="relu"),
            keras.layers.Dense(10, activation="softmax")
        ])

        self.model.compile(optimizer="adam", loss="sparse_categorical_crossentropy",
                           metrics=["accuracy"])

        self.model.fit(train_images, train_labels, epochs=5)

        self.model.save(modelLocation)

    def check(self, array):
        guess = self.model.predict([array])
        print(guess[0])
        num = np.argmax(guess[0])
        return [num, truncate((guess[0][num])*100, 3)]
