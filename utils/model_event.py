import os
import argparse
import sys
import json
from pathlib import Path
from keras.models import load_model

model_default = "default_model.h5"
model_name_default = "default_model"
model_extensions = ["h5"]

root_dir = Path(__file__).parents[1]  # The root directory (mlclassification)
model_dir = os.path.join(root_dir, "models")  # the models directory


def model_delete(model_file):
    if os.path.isdir('./models/'+model_file):
        print("This is a directory. Input a file name")
        result = json.dumps(
            {"error": "true", "message": "This is a directory. Input a file name"})
        return json.loads(result)
    elif os.path.isfile('./models/'+model_file):
        if model_file.split('.')[1].lower() not in model_extensions:
            print("Error: A model file is required. Try again")
            result = json.dumps(
                {"error": "true", "message": "Error: A model file is required. Try again"})
            return json.loads(result)
        if(model_file == model_default):
            print("Error: Can't delete default model")
            result = json.dumps(
                {"error": "true", "message": "Can't delete default model"})
            return json.loads(result)
        os.remove(model_file)
        print('Error: "{} has been deleted".format(model_file)')
        result = json.dumps(
            {"error": "false", "message": "{} has been deleted".format(model_file)})
        return json.loads(result)
    print('Error: Invalid path. Kindly supply a valid folder or image path')
    result = json.dumps(
        {"error": "true", "message": "Invalid path. Kindly supply a valid folder or image path"})
    return json.loads(result)


def all_models():

    all_models = []  # List of all the models in the models directory

    for folder_name, folders, files in os.walk(model_dir):
        for file in files:
            if file.split('.')[1].lower() == 'h5':
                all_models.append(file)
    print(all_models)
    result = json.dumps(
        {"error": "false", "data": all_models})
    return json.loads(result)


def import_model(model_name=model_name_default):
    model = model_dir+'/'+model_name
    classifier = load_model(model)

    return classifier
