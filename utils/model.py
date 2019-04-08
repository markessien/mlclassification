import os
from utils.constants import default_model, model_dir, model_extension


def model_delete(model_file):

    model_file = os.path.join(model_dir, model_file)
    
    if os.path.isfile(model_file):
        if not model_file.endswith(model_extension):
            print("Error: A .h5 model file is required. Try again\n")
            return
        if(model_file == default_model):
            print("Can't delete default model")
            return
        os.remove(model_file)
        print("{} has been deleted".format(model_file))
        return
    print('Error: Invalid path. Kindly supply a valid model\n')
    return

def all_models(default=False):

    if default:
        return default_model

    all_models = [] # List of all the models in the models directory

    for folder_name, folders, files in os.walk(model_dir):
        for file in files:
            if file.split('.')[1].lower() == 'h5':
                all_models.append(file)
                
    return all_models


def import_model(model_name):

    model_path = os.path.join(model_dir, model_name)
    classifier = load_model(model_path)

    return classifier

