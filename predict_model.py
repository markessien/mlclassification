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


def import_model():
    classifier = load_model("model.h5")
    return classifier


def test(classifier, test_img):
    print("testing")
    test_image = prepImage(test_img)
    result = classifier.predict(test_image)
    return printResult(result)


def prepImage(testImage):
    test_image = image.load_img(testImage, target_size=(64, 64))
    test_image = image.img_to_array(test_image)
    test_image = np.expand_dims(test_image, axis=0)
    return test_image


def printResult(result):
    print(result)
    training_set.class_indices
    if result[0][0] >= 0.5:
        prediction = True
    else:
        prediction = False
    return prediction
