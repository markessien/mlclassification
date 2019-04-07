# Python 3.6.7
# Ubuntu 18.04

import os
import json
import sys
import argparse

import shutil

from utils.train_model import train
from utils.predict_model import test, import_model, all_models


file_name = 'classification_results.json'  # the file name
image_extensions = ('jpeg', 'png', 'jpg', 'tiff', 'gif')  # add others


# As there's no other model in the models directory, this will be the best_weights.h5 model
default_model = all_models()[0]


# Use the default one if no one is supplied by the user
def predictor(input_type, folder_or_image, model=default_model):
    """
    Accepts either a folder or an image. Optionally accepts a model argument
    that's the ML model to use for the predictor. If not given, then one of the
    pretrained models from Keras or whatever library is used.
    If an image is given as input, predicts whether the image is a hotel or not
    and prints to the terminal
    If a folder is supplied, loops through all the files in the folder and
    creates a .json file containing a list of all images that are hotels and
    not hotels
    """

    # Load the user-supplied model or the default one
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
        with open(os.path.join(folder_name, file_name), 'w') as f:
            json.dump({os.path.basename(folder_name): prediction,
                       'not_' + os.path.basename(folder_name): not_prediction}, f)
       
        prediction.clear() # clear the list containing the prediction names for use in the next iterated folder
        not_prediction.clear()  # Do the same for the not_prediction list

    return


def parse_args(argv):
    parser = argparse.ArgumentParser("")
    parser.add_argument(
        'app_action',
        help='This can either be predict or train',
        default='predict'
    )
    parser.add_argument(
        '--path',
        help='A path to a folder or image(optional) e.g /hotels or newhotel.jpg'
    )
    parser.add_argument(
        '-trp',
        '--train_folder_path',
        help = 'A training folder path e.g dataset/training_set'
    )
    parser.add_argument(
        '-tep',
        '--test_folder_path',
        help = 'A test folder path e.g dataset/test_set'
    )
    parser.add_argument(
        '--model',
        help='Selects a model to be used',
        )
    return parser.parse_args(argv[1:])


def main(argv=sys.argv):
    """ The main script """

    input_type = None
    args = parse_args(argv)
    folder_or_image = args.path
    action = args.app_action

    model_name = "{}.h5".format(args.model)
    all_model_path = "./model"
    if model_name not in os.listdir(all_model_path):
        print('\nModel does not exist. Please choose a model.')
        return

    train_folder_path = args.train_folder_path
    test_folder_path = args.test_folder_path
    if action == 'train':
        #Check that both train and test folders are present
        if train_folder_path:
            # If train folder is provided, test folder must also be provided
            if test_folder_path:
                train(model_name, train_folder=train_folder_path, test_folder=test_folder_path)
            print('\n You cannot provide only one folder. Provide training folder and testing folder or None')
            return #You must return  
        if test_folder_path:
            #Means test folder was provided but not train folder
            print('\n You cannot provide only one folder. Provide training folder and testing folder or None')
            return #You must return
        else:
            # Means no folder was provided, run with default
            train(model_name)
    elif action == 'predict' and folder_or_image is None:
        print('\n A path to a folder or image is required e.g /hotels or newhotel.jpg \n for help: run python3 app.py -h')
        return
    elif action == 'predict':
        # if it's not a folder that was supplied, check if it's a file
        if not os.path.isdir(folder_or_image):
            if os.path.isfile(folder_or_image):
                if folder_or_image.split('.')[1].lower() not in image_extensions:
                    print("\nError: An image file is required. Try again\n")
                    return
                input_type = 'file'
                # add logic before here to pass in the model we want to use in the predictor
                predictor(input_type, folder_or_image)
                return
            print('\nError: Invalid path. Kindly supply a valid folder or image path\n')
            return

        input_type = 'folder'

        # add logic before here to pass in the model we want to use in the predictor
        predictor(input_type, folder_or_image)
        if input_type == 'folder':
            print(
                f"\nDone! The '{file_name}' file has been written to respective folders in {folder_or_image}")

    else:
        print('\nAction command is not supported\n for help: run python3 app.py -h')


if __name__ == '__main__':
    main()
