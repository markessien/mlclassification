import os
import sys
import numpy as np
import shutil
import json
from keras.preprocessing import image
from keras.preprocessing.image import ImageDataGenerator
from tqdm import tqdm
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
    model = os.path.join(model_dir,model)
    classifier = import_model(model)

    if input_type == 'file':

        # Removed the file type vaildation that was here before because it's already done in the argparser place.
        # No need for redundancy
        outcome = test(classifier, folder_or_image)

        if outcome == True:
            print("\nThe image does not correspond with sorted image for Group A in this model")
            sys.stdout.flush()
            return

        print("\nThis image correspond with the sorted images for Group B in this model")
        sys.stdout.flush()
        return  # important. Must return

    # It's implicit that the input type is a folder from here on
    folder_ = folder_or_image
    prediction = []  # list of file names that are the prediction
    not_prediction = []  # list of file names that are not the prediction
    #First create prediction folder inside provided folder
    main_prediction_folder = os.path.join(folder_,'predictions')
    if os.path.isdir(main_prediction_folder):
        shutil.rmtree(main_prediction_folder)
    os.mkdir(main_prediction_folder)
    # Make the prediction and not prediction folders (just thier paths)
    # I used some form of dynamic naming here to create the folder names
    # Please feel free to change it to something more suitable.
    # I simply used the folder name of the current folder being checked as
    # the prediction folder and then added 'not_' to that name for the
    # not_prediction folder. So if 'hotels' was being checked, the folder
    # names for the predictions would be 'hotels' and 'not_hotels'
    # Kindly change as deemed.
        
    prediction_folder = os.path.join(
            main_prediction_folder, os.path.basename(folder_))
    not_prediction_folder = os.path.join(
            main_prediction_folder, 'not_' + os.path.basename(folder_))
        
    # Create the folders using their paths
    os.mkdir(prediction_folder)
    os.mkdir(not_prediction_folder)
    #We need to exclude the prediction folder as we walk the provided directory
    exclude = set(['predictions'])
    for root, dirs, files in os.walk(folder_):
        # Below code modifies dirs in place using the default topdown=True, check os.walk help doc
        dirs[:]= [d for d in dirs if d not in exclude]
        
        for file in tqdm(files):

            # Didn't remove the file-type validation here as some files in the supplied
            # directory may not be images, unlike up where only an image is supplied.
            if file.lower().endswith(image_extensions):
                outcome = test(classifier, os.path.join(root, file))

                # Add to JSON list and then copy it to its respective folder
                if outcome == True:
                    not_prediction.append(file)
                    shutil.copy(os.path.join(root, file),
                                not_prediction_folder)
                else:
                    prediction.append(file)
                    shutil.copy(os.path.join(root, file),
                                prediction_folder)

        # Then actually write to JSON (Since we are still using JSON)
        with open(os.path.join(main_prediction_folder, json_file), 'w') as f:
            json.dump({os.path.basename(root): prediction,
                       'not_' + os.path.basename(root): not_prediction}, f)
       
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
