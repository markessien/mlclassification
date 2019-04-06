
# Python 3.6.7
# Ubuntu 18.04

import os
import sys
import json
from predict_model import test, import_model

file_name = 'classification_results.json'  # the file name
image_extensions = ('jpeg', 'png', 'jpg', 'tiff', 'gif')  # add others

classifier = import_model()
# model argument can be substituted with a model of ours


def predictor(input_type, folder_or_image, model=None):
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

    classifier = import_model()
    if input_type == 'file':

        # Apply directly the ML classifier to predict the output
        # Do all that and return
        if folder_or_image.lower().endswith(image_extensions):
            outcome = test(classifier, folder_or_image)
            if outcome == True:
                print('Not Hotel')
                return

            print('Hotel')
            return  # important. Must return
        print('Unsupported file type')
    # It's implicit that the input type is a folder from here on

    hotels = []  # list of file names that are hotels
    not_hotels = []  # list of file names that are not hotels

    for folder_name, folders, files in os.walk(folder_or_image):

        for file in files:

            # Apply ML classifier logic to all files in the folder
            # Categorize result based on the prediction
            # Just an example. The below line will be replaced with the actual ML logic
            # print(folder_name+'/'+file)
            if file.lower().endswith(image_extensions):
                outcome = test(classifier, folder_name+'/'+file)
                if outcome == True:
                    not_hotels.append(file)
                else:
                    hotels.append(file)

        # After each iteration in a folder,
        with open(os.path.join(folder_name, file_name), 'w') as f:
            # write result to a json file in the folder
            json.dump({'hotels': hotels, 'not_hotels': not_hotels}, f)

        hotels.clear()  # clear the list containing the hotel names for use in the next iterated folder
        not_hotels.clear()  # Do the same for the not_hotels list

    return


def main():
    """ The main script """

    input_type = None

    while 1:
        
        try: sys.argv[1]
        except IndexError: x = None
        if x is None:
            return print('A file or folder is compulsory')
        folder_or_image = sys.argv[1]
        print(folder_or_image)
        # if it's not a folder that was supplied, check if it's a file
        if not os.path.isdir(folder_or_image):
            if os.path.isfile(folder_or_image):
                if folder_or_image.split('.')[1].lower() not in image_extensions:
                    print("Error: An image file is required. Try again\n")
                    continue

                input_type = 'file'
                break

            print('Error: Invalid path. Kindly supply a valid folder or image path\n')
            continue

        input_type = 'folder'
        break

    # add logic before here to pass in the model we want to use in the predictor
    predictor(input_type, folder_or_image)

    if input_type == 'folder':
        print(
            f"Done! The '{file_name}' file has been written to respective folders in {folder_or_image}")


if __name__ == '__main__':
    main()
