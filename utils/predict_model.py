

# Importing the Keras libraries and packages

import os
import keras
import numpy as np
import tensorflow as tf
from keras.models import load_model

from pathlib import Path

from keras.preprocessing import image
from keras.preprocessing.image import ImageDataGenerator

from keras.models import Sequential, load_model
from keras.layers import Conv2D, MaxPooling2D, Flatten, Dense

#module for evaluation metrixs
from sklearn.metrics import accuracy_score, classification_report, classification_report, confusion_matrix

root_dir = Path(__file__).parents[1] # The root directory (mlclassification)
model_dir = os.path.join(root_dir, "models") # the models directory


train_datagen = ImageDataGenerator(
    rescale=1./255,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True
)

test_datagen = ImageDataGenerator(rescale=1./255)


def all_models():

    all_models = [] # List of all the models in the models directory

    for folder_name, folders, files in os.walk(model_dir):
        for file in files:
            if file.split('.')[1].lower() == 'h5':
                all_models.append(file)

    return all_models


def import_model(model_name):

    classifier = load_model(model_name)

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


def evaluation_metrix():
    classifier = import_model(model_name)
    test_image = prepImage(testImage)
    evaluator = test(classifier, test_img)  
    accuracyScore = accuracy_score(test_image, evaluator, normalize=False)
    classificationReport = classification_report(test_image, evaluator, target_names =['0','1'])
    confusionMatrix = confusion_matrix(test_image, evaluator, labels=[0,1], normalize=False)
    
    return accuracyScore, confusionMatrix, classificationReport
