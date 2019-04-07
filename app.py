# Python 3.6.7


import os
import json
import sys
import argparse

import shutil

from utils.train_model import train
from utils.predict_model import test, import_model, all_models
from utils.model import model_delete

from utils.constants import model_extension, default_model

file_name = 'classification_results.json'  # the file name
image_extensions = ('jpeg', 'png', 'jpg', 'tiff', 'gif')  # add others


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
        help='This can either be predict, train, models or delete',
        default='predict'
    )
    parser.add_argument(
        '-p',
        '--path',
        help='A path to a folder or image e.g hotels or newhotel.jpg'
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
        '-m',
        '--model',
        help="A model name to use e.g catdogmodel or my_model (no need to add the extension)"
    )
    
    return parser.parse_args(argv[1:])


def main(argv=sys.argv):
    """ The main script """

    args = parse_args(argv)

    action = args.app_action

    # If the action is train, the model is the name of the new model
    # that is going to be trained; if it's predict, the model is the
    # name of the model to use for prediction
    model = args.model 

    if action == 'train': 
        # Instead of the folder_paths being None if they were not supplied
        # make them empty strings so the os.path functions below won't 
        # throw errors
        train_folder_path = "" if args.train_folder_path is None else args.train_folder_path
        test_folder_path = "" if args.test_folder_path is None else args.test_folder_path

        new_model = model

        if not new_model:
            print("Kindly give a name to save your model with")
            return
        
        if new_model + model_extension in all_models():
            print("There's already a model with that name. Choose another name")
            return
                
        # Check that both train and test folders are present (Catch both orders)
        if os.path.isdir(train_folder_path):

            # If train folder is provided first, test folder must also be provided
            if os.path.isdir(test_folder_path):
                train(new_model, train_folder=train_folder_path, test_folder=test_folder_path)

            print('\n You cannot provide only one folder. Provide both training and testing folder')
            return # You must return  

        # If test folder is provided, check is train folder is also provided
        if os.path.isdir(test_folder_path):
            if os.path.isdir(train_folder_path):
                train(new_model, train_folder=train_folder_path, test_folder=test_folder_path)

            print('\n You cannot provide only one folder. Provide both training and testing folder')
            return # You must return
        
        # Means no folder was provided, run with default folders
        train(new_model)

    elif action == 'predict':

        folder_or_image = "" if args.path is None else args.path

        # If no model was given, use the default one
        if not model:
            model = default_model
        
        else:
            # If one was supplied, check that it actually exists
            if model + model_extension not in all_models():
                print("No such model has been trained")
                return

        # if it's not a folder that was supplied, check if it's a file
        if not os.path.isdir(folder_or_image):
            if os.path.isfile(folder_or_image):
                if not folder_or_image.endswith(image_extensions):
                    print("\nError: An image file is required. Try again\n")
                    return
                input_type = 'file'
                # add logic before here to pass in the model we want to use in the predictor
                predictor(input_type, folder_or_image, model)
                return
            print('\nError: Invalid path. Kindly supply a valid folder or image path\n')
            return

        input_type = 'folder'

        # add logic before here to pass in the model we want to use in the predictor
        predictor(input_type, folder_or_image, model)
        if input_type == 'folder':
            print(
                f"\nDone! The results are in {folder_or_image}")

    elif action == 'delete':
        # Check that model name is provided. 

        if not model:
            print("\n You must supply a model to delete")
            return
            
        if model + model_extension not in all_models():
            print("That model does not exist")
            return

        model_delete(model)
        return
    elif action == 'models':
        #list all models
        print(all_models)
        return
    else:
        print('\nAction command is not supported\n for help: run python3 app.py -h')


if __name__ == '__main__':
    main()
