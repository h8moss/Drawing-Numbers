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
"""
data = keras.datasets.mnist

(train_images, train_labels), (test_images, test_labels) = data.load_data()

# Scaling images from 0-255 to 0-1
train_images = train_images / 255.0
test_images = test_images / 255.0

if os.path.exists("./Model.h5"):
    model = tf.keras.models.load_model('Model.h5')
else:
    model = keras.Sequential([
            keras.layers.Flatten(input_shape=(28, 28)),
            keras.layers.Dense(128, activation="relu"),
            keras.layers.Dense(10, activation="softmax")
        ])
    
    model.compile(optimizer="adam", loss="sparse_categorical_crossentropy", metrics=["accuracy"])
    
    model.fit(train_images, train_labels, epochs=7)
    
    model.save('./Model.h5') 

test_loss, test_acc = model.evaluate(test_images, test_labels)

prediction = model.predict(test_images)
"""
class Model():

    def __init__(self):
        self.data = keras.datasets.mnist
        if os.path.exists("./Model.h5"):
            self.model = tf.keras.models.load_model('Model.h5')
        else:
            self.MakeModel()

    def MakeModel(self):
        #TODO: Don't separate into test and train, you only want to train
        (train_images, train_labels), (test_images, test_labels) = self.data.load_data()
        model = keras.Sequential([
            keras.layers.Flatten(input_shape=(28, 28)),
            keras.layers.Dense(128, activation="relu"),
            keras.layers.Dense(10, activation="softmax")
        ])
    
        model.compile(optimizer="adam", loss="sparse_categorical_crossentropy", 
        metrics=["accuracy"])
    
        model.fit(train_images, train_labels, epochs=7)
    
        model.save('./Model.h5') 

    def check(self, array):
        guess = 0
        guess = self.model.predict([array])
        num = np.argmax(guess[0])
        return [num, truncate((guess[0][num]/1)*100, 3)]
