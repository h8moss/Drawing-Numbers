import tensorflow as tf
from tensorflow import keras
import numpy as np
import matplotlib.pyplot as plt
import pickle
import os

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

for i in range(10):
    plt.grid(False)
    plt.imshow(test_images[i], cmap=plt.cm.binary)
    plt.xlabel("Actual: " + str(test_labels[i]))
    plt.title("Prediction: " + str(np.argmax(prediction[i])))
    plt.show()
