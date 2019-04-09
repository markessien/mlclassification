import os
import json
import sys
import argparse
from utils.train_model import train
from utils.train_model import train_model #Validator for train function
from utils.predict_model import predictor
from utils.model import model_delete
from utils.model import import_model
from utils.model import all_models
from utils.model import generate_name
from utils.constants import default_model
from utils.constants import model_dir
from utils.constants import model_extension
from utils.constants import image_extensions
from utils.constants import truth_values



def parse_args(argv):
    parser = argparse.ArgumentParser("")
    parser.add_argument(
        'app_action',
        help='This can either be predict, train, retrieve_models or delete',
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
    parser.add_argument(
        '--gen_name',
        help = 'A boolean to generate model name e.g yes or no',
        default = 'no'
    )

    return parser.parse_args(argv[1:])

def main(argv=sys.argv):
    """ The main script """

    args = parse_args(argv)

    action = args.app_action
    train_folder_path =args.trp
    test_folder_path = args.tep
    folder_or_image = "" if args.path is None else args.path
    #Any arg supplied to this will be seen as True, no arg means False
    generate_model_name = args.gen_name 

    # If the action is train, the model is the name of the new model
    # that is going to be trained; if it's predict, the model is the
    # name of the model to use for prediction
    model = args.model 

    if action == 'train': 
        
        new_model = model
        if not new_model:
            if generate_model_name in truth_values:
                #The user want us to generate model name for them
                #trp and tep args are required args implicitly for users from app
                if train_folder_path and test_folder_path:
                    #Means user fulfilled the requirement. we can proceed now
                    #generate name
                    new_model = generate_name(train_folder_path)
                    train_model(new_model, train_folder_path, test_folder_path)
                    return
                #Here, the user might have supplied one folder argument or None at all
                print("\n Both training folder and test folder arguments are required")
                return
            #The user did not supply model name and did not ask us to generate one. So definitely, 
            # we are the one running this from console app
            #We don't want to retrain our default model. Better to delete. So we have to check if we
            #have trained our default model before. If default model exist, return
            if default_model in all_models():
                print("Retraining the default model is forbidden. Supply model name or Delete the default model manually and proceed")
                return
                
            #Training our default model now
            new_model = default_model
            print("Training the default model now...")
            #We use train function directly here for obvious reasons
            return train(new_model)
        
        #Model name supplied
        new_model = model + model_extension
        if new_model in all_models():
            print("There's already a model with that name. Please choose another name"
             " or find a model with name {}. Delete it and try again".format(new_model))
            return
        #From here on, we expect user to supply training dataset and test dataset. 
        #trp and tep args are required args implicitly for users from app
        if train_folder_path and test_folder_path:
            #Means user fulfilled the requirement. we can proceed now   
            return train_model(new_model, train_folder_path, test_folder_path)
        #Here, the user might have supplied one folder argument or None at all
        print("\n Both training folder and test folder arguments are required")
        return 
                



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
