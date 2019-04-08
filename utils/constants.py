
import os
from pathlib import Path

default_model = 'default_model.h5'
root_dir = Path(__file__).parents[1] # The root directory (mlclassification)
model_dir = os.path.join(root_dir, "models") # the models directory
model_extension = ".h5"
file_name = 'classification_results.json'  # the file name
image_extensions = ('jpeg', 'png', 'jpg', 'tiff', 'gif')  # add others
default_train_folder_path='./datasets/training_set'
default_test_folder_path='./datasets/test_set'