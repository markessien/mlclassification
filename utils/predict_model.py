import os
import numpy as np
import shutil
import json
from keras.preprocessing import image
from keras.preprocessing.image import ImageDataGenerator
from utils.constants import default_model
from utils.constants import model_dir
from utils.constants import model_extension
from utils.constants import image_extensions
from utils.constants import json_file
from utils.model import model_delete
from utils.model import import_model
from utils.model import all_models

# Use the default one if no one is supplied by the user
def predictor(input_type, folder_or_image, model):
    """
    Accepts either a folder or an image, and a model argument that's the ML model
    to use for the function. 

    """

    # Load the model
    classifier = import_model(model)

    if input_type == 'file':

        # Removed the file type vaildation that was here before because it's already done in the argparser place.
        # No need for redundancy
        outcome = test(classifier, folder_or_image)

        if outcome == True:
            print('\nNot Hotel')
            return

        print('\nHotel')

        return  # important. Must return

    # It's implicit that the input type is a folder from here on

    prediction = []  # list of file names that are the prediction
    not_prediction = []  # list of file names that are not the prediction

    for folder_name, folders, files in os.walk(folder_or_image):

        # Make the prediction and not prediction folders (just thier paths)
        # I used some form of dynamic naming here to create the folder names
        # Please feel free to change it to something more suitable.
        # I simply used the folder name of the current folder being checked as
        # the prediction folder and then added 'not_' to that name for the
        # not_prediction folder. So if 'hotels' was being checked, the folder
        # names for the predictions would be 'hotels' and 'not_hotels'
        # Kindly change as deemed.
        prediction_folder = os.path.join(
            folder_name, os.path.basename(folder_name))
        not_prediction_folder = os.path.join(
            folder_name, 'not_' + os.path.basename(folder_name))

        # Create the folders using their paths
        os.mkdir(prediction_folder)
        os.mkdir(not_prediction_folder)

        for file in files:

            # Didn't remove the file-type validation here as some files in the supplied
            # directory may not be images, unlike up where only an image is supplied.
            if file.lower().endswith(image_extensions):
                outcome = test(classifier, os.path.join(folder_name, file))

                # Add to JSON list and then copy it to its respective folder
                if outcome == True:
                    not_prediction.append(file)
                    shutil.copy(os.path.join(folder_name, file),
                                not_prediction_folder)
                else:
                    prediction.append(file)
                    shutil.copy(os.path.join(folder_name, file),
                                prediction_folder)

        # Then actually write to JSON (Since we are still using JSON)
        with open(os.path.join(folder_name, json_file), 'w') as f:
            json.dump({os.path.basename(folder_name): prediction,
                       'not_' + os.path.basename(folder_name): not_prediction}, f)
       
        prediction.clear() # clear the list containing the prediction names for use in the next iterated folder
        not_prediction.clear()  # Do the same for the not_prediction list

    return

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
