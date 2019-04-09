import os
from utils.constants import default_model
from utils.constants import model_dir
from utils.constants import model_extension
from keras.models import load_model

def model_delete(model_file):

    _model_file = os.path.join(model_dir, model_file)
    
    if os.path.isfile(_model_file):
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


def disambiguate_name(name):
    parts = name.split('-')
    if len(parts) > 1:
        try:
            index = int(parts[-1])
        except ValueError:
            parts.append('1')
        else:
            parts[-1] = ""+str(index + 1)

    else:
        parts.append('1')
    return '-'.join(parts)

def generate_name(train_folder_path):
    backlist = [name.split('.')[0] for name in all_models()] #strip out extensions
    #check if train_folder_path is directory
    if os.path.isdir(train_folder_path):
        name1 = os.path.basename(train_folder_path)
        name = name1+'_not'+name1
        while name in backlist:
            name = disambiguate_name(name)
        return name+model_extension
    print("Provided path is not a directory")
    return