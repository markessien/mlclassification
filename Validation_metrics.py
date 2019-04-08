
#%%
from keras.models import load_model
from keras.preprocessing import image
from keras.preprocessing.image import load_img, img_to_array
import numpy as np
import os
from pathlib import Path

image_extensions = ('jpeg', 'png', 'jpg', 'tiff', 'gif')

def prepImage(image):
    test_image = load_img(image, target_size=(64, 64))
    test_image = img_to_array(test_image)
    test_image = np.expand_dims(test_image, axis=0)
            
    return test_image

def prepFolder(folder):
    if os.path.isdir(folder):
        directory = os.fsencode(folder)
        for images in os.listdir(directory):
            image = os.fsdecode(images)
            path = os.path.join(folder, image)
            array = prepImage(path)
        return array
    return prepImage(folder)

def validation_metrics (folder_or_image, y):
    model = load_model('models/default_model.h5')
    array = prepFolder(folder_or_image)
    if isinstance (array, list):
        y = [1] * len(array)
        y = np.array(y).reshape(-1,1)
    y = np.array(y).reshape(-1,1)S

    metrics = model.evaluate(array, y)
    return model.metrics_names, metrics
