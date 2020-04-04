import tensorflow as tf
from tensorflow import keras
import numpy as np
import matplotlib.pyplot as plt
import pickle
import os
import math


def truncate(number, digits) -> float:
    stepper = 10.0 ** digits
    return math.trunc(stepper * number) / stepper


class Model():

    def __init__(self):
        self.data = keras.datasets.mnist
        if os.path.exists("./python/Model.h5"):
            self.model = tf.keras.models.load_model('./python/Model.h5')
        else:
            self.MakeModel()

    def MakeModel(self):
        #TODO: Don't separate into test and train, you only want to train
        (train_images, train_labels), (test_images, test_labels) = self.data.load_data()
        self.model = keras.Sequential([
            keras.layers.Flatten(input_shape=(28, 28)),
            keras.layers.Dense(128, activation="relu"),
            keras.layers.Dense(10, activation="softmax")
        ])
    
        self.model.compile(optimizer="adam", loss="sparse_categorical_crossentropy", 
        metrics=["accuracy"])
    
        self.model.fit(train_images, train_labels, epochs=7)
    
        self.model.save('./python/Model.h5') 

    def check(self, array):
        guess = 0
        guess = self.model.predict([array])
        num = np.argmax(guess[0])
        return [num, truncate((guess[0][num]/1)*100, 3)]
