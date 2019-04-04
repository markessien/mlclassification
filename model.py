# Importing the Keras libraries and packages
import numpy as np
import keras
import tensorflow as tf
from keras.models import load_model
from IPython.display import display
from PIL import Image
from keras.preprocessing import image
from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential
from keras.layers import Conv2D
from keras.layers import MaxPooling2D
from keras.layers import Flatten
from keras.layers import Dense


train_datagen = ImageDataGenerator(
    rescale=1./255,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True
)

test_datagen = ImageDataGenerator(rescale=1./255)

training_set = train_datagen.flow_from_directory('./training_set', target_size=(64, 64),
                                                 batch_size=32,
                                                 class_mode='binary')
test_set = test_datagen.flow_from_directory('./test_set',
                                            target_size=(64, 64),
                                            batch_size=32,
                                            class_mode='binary')


def train():
    print("Training")
    classifier = Sequential()

    # Step 1 - Convolution
    classifier.add(
        Conv2D(32, (3, 3), input_shape=(64, 64, 3), activation='relu'))
    # Step 2 - Pooling
    classifier.add(MaxPooling2D(pool_size=(2, 2)))

    # Adding a second convolutional layer
    classifier.add(Conv2D(32, (3, 3), activation='relu'))
    classifier.add(MaxPooling2D(pool_size=(2, 2)))
    # Step 3 - Flattening
    classifier.add(Flatten())

    # Step 4 - Full connection
    classifier.add(Dense(units=128, activation='relu'))
    classifier.add(Dense(units=1, activation='sigmoid'))
    # Compiling the CNN
    classifier.compile(
        optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

    classifier.fit_generator(training_set,
                             steps_per_epoch=8000,
                             epochs=25,
                             validation_data=test_set,
                             validation_steps=2000)

    classifier.save("model.h5")


def test(test_img):
    print(test_img)
    print("testing")
    classifier = load_model("model.h5")
    print("\nModel Loaded\n")
    test_image = prepImage(test_img)
    result = classifier.predict(test_image)
    return printResult(result)


def prepImage(testImage):
    test_image = image.load_img(testImage, target_size=(64, 64))
    test_image = image.img_to_array(test_image)
    test_image = np.expand_dims(test_image, axis=0)
    return test_image


def printResult(result):
    training_set.class_indices
    if result[0][0] == 1:
        prediction = 'Hotel'
    else:
        prediction = 'Not Hotel'
    return prediction


def setupTF():
    print("Setting up GPU TensorFlow")
    config = tf.ConfigProto(device_count={'GPU': 1})
    sess = tf.Session(config=config)
    keras.backend.set_session(sess)

