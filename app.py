# Python 3.6.7
# Ubuntu 18.04

import os
import json
import sys
import argparse
from controllers.predict_model import predictor
from controllers.train_model import train
from utils.model_event import import_model, all_models, model_delete


file_name = 'classification_results.json'  # the file name
image_extensions = ('jpeg', 'png', 'jpg', 'tiff', 'gif')  # add others


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
        help='A training folder path e.g dataset/training_set'
    )
    parser.add_argument(
        '-tep',
        help='A test folder path e.g dataset/test_set'
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
    train_folder_path = args.trp
    test_folder_path = args.tep
    model_name = "{}.h5".format(args.model)
    all_model_path = "./models/"

    if action == 'train':
        # Check that both train and test folders are present
        if train_folder_path and test_folder_path:
            train(model_name, train_folder=train_folder_path,
                  test_folder=test_folder_path)
        else:
            # Means no folder was provided, run with default
            train(model_name)
    elif action == 'predict':
        if model_name not in os.listdir(all_model_path):
            print('\nModel does not exist. Please choose a model.')
            result = json.dumps(
                {"error": "true", "message": "Model does not exist. Please choose a model."})
            return json.loads(result)
        # if it's not a folder that was supplied, check if it's a file
        if not os.path.isdir(folder_or_image):
            if os.path.isfile(folder_or_image):
                if folder_or_image.split('.')[1].lower() not in image_extensions:
                    print("\nError: An image file is required. Try again\n")
                    result = json.dumps(
                        {"error": "true", "message": "An image file is required. Try again"})
                    return json.loads(result)
                input_type = 'file'
                # add logic before here to pass in the model we want to use in the predictor
                predictor(input_type, folder_or_image, model_name)
                return
            print('\nError: Invalid path. Kindly supply a valid folder or image path\n')
            result = json.dumps(
                {"error": "true", "message": "Invalid path. Kindly supply a valid folder or image path"})
            return json.loads(result)

        input_type = 'folder'
        # add logic before here to pass in the model we want to use in the predictor
        predictor(input_type, folder_or_image, model_name)
        if input_type == 'folder':
            print(
                f"\nDone! The '{file_name}' file has been written to respective folders in {folder_or_image}")
            result = json.dumps(
                {"error": "false", "message":  f"Done! The '{file_name}' file has been written to respective folders in {folder_or_image}"})
            return json.loads(result)
    elif action == 'delete':
        if model_name not in os.listdir(all_model_path):
            print('\nModel does not exist. Please choose a model.')
            result = json.dumps(
                {"error": "true", "message": "Model does not exist. Please choose a model."})
            return json.loads(result)
        return model_delete(model_name)
    elif action == 'retrieve_models':
        return all_models()
    else:
        print('\nAction command is not supported\n for help: run python3 app.py -h')
        result = json.dumps(
            {"error": "true", "message": "Action command is not supported for help: run python3 app.py -h"})
        return json.loads(result)


if __name__ == '__main__':
    main()
