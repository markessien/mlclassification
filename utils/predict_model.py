

# Importing the Keras libraries and packages

import os

from keras.preprocessing import image
from keras.preprocessing.image import ImageDataGenerator

from keras.models import load_model

from .constants import model_default, model_dir



def all_models(default=False):

    if default:
        return model_default

    all_models = [] # List of all the models in the models directory

    for folder_name, folders, files in os.walk(model_dir):
        for file in files:
            if file.split('.')[1].lower() == 'h5':
                all_models.append(file)

    return all_models


def import_model(model_name):
    
    model_path = os.path.join(model_dir, model_name)
    classifier = load_model(model_path)

    return classifier


def test(classifier, test_img):

    test_image = prepImage(test_img)
    result = classifier.predict(test_image)
    return printResult(result)


def prepImage(testImage):

    test_image = image.load_img(testImage, target_size=(64, 64))
    test_image = image.img_to_array(test_image)
    test_image = np.expand_dims(test_image, axis=0)

    return test_image


def printResult(result):
    if result[0][0] == 1:
        prediction = True
    else:
        prediction = False

    return prediction
