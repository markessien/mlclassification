import keras
from keras.models import Sequential
from keras.preprocessing import image
from keras.models import load_model
from keras.layers import Convolution2D, MaxPooling2D, Flatten, Dense
from keras.preprocessing.image import ImageDataGenerator
from IPython.display import display
import numpy as np

import tensorflow as tf

train_datagen = ImageDataGenerator(
    rescale=1./255,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True
)

training_set = train_datagen.flow_from_directory(
    'training_images/hotels/training_images',
    target_size=(64, 64),
    batch_size=8,
    class_mode='binary'
)

test_datagen = ImageDataGenerator(rescale=1./255)

test_set = test_datagen.flow_from_directory(
    'training_images/hotels/test_images',
    target_size=(64, 64),
    batch_size=8,
    class_mode='binary'
)


def train():
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
        training_set,
        steps_per_epoch=2000,
        epochs=5,
        validation_data=test_set,
        validation_steps=200
    )

    classifier.save("model.h5")


def test():
    print("testing")
    classifier = load_model("model.h5")
    print("\nModel Loaded\n")
    test_image = prepImage("not_hotels/1.png")
    result = classifier.predict(test_image)
    printResult(result)
    test_image = prepImage("not_hotels/6.png")
    result = classifier.predict(test_image)
    printResult(result)
    test_image = prepImage("not_hotels/5.png")
    result = classifier.predict(test_image)
    printResult(result)


def prepImage(testImage):
    test_image = image.load_img(testImage, target_size=(64, 64))
    test_image = image.img_to_array(test_image)
    test_image = np.expand_dims(test_image, axis=0)
    return test_image


def printResult(result):
    training_set.class_indices
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


train()
# def main(isGPU, train):
#     if isGPU :
#         setupTF()

#     if train:
#         train()
#     else:
#         test()


# main(True,True)
