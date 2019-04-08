# Python 3.6.7


import os
import json
import sys
import argparse
from controllers.train_model import train_model
from controllers.predict_model import predictor
from utils.model import model_delete,import_model,all_models
from utils.constants import default_model, model_dir,model_extension,image_extensions,file_name,default_test_folder_path,default_train_folder_path



def parse_args(argv):
    parser = argparse.ArgumentParser("")
    parser.add_argument(
        'app_action',
        help='This can either be predict, train, models or delete',
        default='predict'
    )
    parser.add_argument(
        '--path',
        help='A path to a folder or image e.g /foo or foobar.jpg'

    )
    parser.add_argument(
        '--trp',
        help='A training folder path e.g dataset/training_set'
    )
    parser.add_argument(
        '--tep',
        help='A test folder path e.g dataset/test_set'
    )
    parser.add_argument(
        '--model',
        help='Selects a model to be used',
    )

    return parser.parse_args(argv[1:])

def main(argv=sys.argv):
    """ The main script """

    args = parse_args(argv)

    action = args.app_action
    train_folder_path =args.trp
    test_folder_path = args.tep
    folder_or_image = "" if args.path is None else args.path

    # If the action is train, the model is the name of the new model
    # that is going to be trained; if it's predict, the model is the
    # name of the model to use for prediction
    model = args.model 

    if action == 'train': 
        # Instead of the folder_paths being None if they were not supplied
        # make them empty strings so the os.path functions below won't 
        # throw errors
        new_model = model
        if not new_model:
            new_model = default_model
            print("No name provided: Using default model")
            train_folder_path_used = default_train_folder_path if train_folder_path is None  else train_folder_path
            test_folder_path_used = default_test_folder_path if test_folder_path is None  else test_folder_path
            return train_model(train_folder_path_used,new_model,test_folder_path_used)
        
        new_model = model + model_extension
        if new_model in all_models():
            print("There's already a model with that name. Retraining")
            train_folder_path_used = default_train_folder_path if train_folder_path is None  else train_folder_path
            test_folder_path_used = default_test_folder_path if test_folder_path is None  else test_folder_path
            return train_model(train_folder_path_used,new_model,test_folder_path_used)
                



    elif action == 'predict':

        # If no model was given, use the default one
        if not model:
            model = default_model
        
        else:
            model = model + model_extension
            
            # If one was supplied, check that it actually exists
            if model not in all_models():
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
        
        model = model + model_extension
            
        if model not in all_models():
            print("That model does not exist")
            return

        model_delete(model)

        return

    elif action == 'retrieve_models':

        # List all models
        print(all_models())

        return


    else:
        print('\nAction command is not supported\n for help: run python3 app.py -h')

if __name__ == '__main__':
    main()
