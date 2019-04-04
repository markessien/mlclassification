import keras
from keras.models import Sequential
from keras.preprocessing import image
from keras.models import load_model
from keras.layers import Convolution2D, MaxPooling2D, Flatten, Dense
from keras.preprocessing.image import ImageDataGenerator
import numpy as np

import tensorflow as tf

from prepare_images import train_generator
from prepare_images import validation_generator



def train(epochs):
    print("Training")
    classifier = Sequential()

    classifier.add(Convolution2D(
        32, 2, 3, input_shape=(64, 64, 3), activation='relu'))

    classifier.add(MaxPooling2D(pool_size=(2, 2)))

    classifier.add(Flatten())

    classifier.add(Dense(output_dim=128, activation='relu'))
    classifier.add(Dense(output_dim=1, activation='sigmoid'))

    classifier.compile(
        optimizer="adam", loss="binary_crossentropy", metrics=['accuracy'])

    classifier.fit_generator(
        train_generator,
        steps_per_epoch=2000,
        epochs=epochs,
        validation_data=validation_generator,
        validation_steps=200
    )

    classifier.save("model.h5")

# Test is not yet passing

def test():
    print("testing")
    classifier = load_model("model.h5")
    print("\nModel Loaded\n")
    test_image = prepImage("validation_data/not-hotels/8.png")
    result = classifier.predict(test_image)
    printResult(result)
    test_image = prepImage("validation_data/not-hotels/14.jpg")
    result = classifier.predict(test_image)
    printResult(result)
    test_image = prepImage("validation_data/not-hotels/038.jpg")
    result = classifier.predict(test_image)
    printResult(result)


def prepImage(testImage):
    test_image = image.load_img(testImage, target_size=(64, 64))
    test_image = image.img_to_array(test_image)
    test_image = np.expand_dims(test_image, axis=0)
    return test_image


def printResult(result):
    train_generator.class_indices
    if result[0][0] >= 0.5:
        prediction = 'hotel'
    else:
        prediction = 'non-hotel'
    print(prediction)


def setupTF():
    print("Setting up GPU TensorFlow")
    config = tf.ConfigProto(device_count={'GPU': 1})
    sess = tf.Session(config=config)
    keras.backend.set_session(sess)

if __name__ == '__main__':
    train(3)
    test()

# def main(isGPU, train):
#     if isGPU :
#         setupTF()

#     if train:
#         train()
#     else:
#         test()


# main(True,True)
