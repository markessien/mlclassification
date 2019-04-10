import os
from pathlib import Path

default_model = 'default_model.h5'
root_dir = Path(__file__).parents[1] # The root directory (mlclassification)
model_dir = os.path.join(root_dir, "models") # the models directory
model_extension = ".h5"
json_file = 'classification_results.json'  # the file name
image_extensions = ('jpeg', 'png', 'jpg', 'tiff')  # add others
default_train_folder_path='./datasets/training_set'
default_test_folder_path='./datasets/test_set'
truth_values = ['yes', 'y','true','1']
false_values = ['no','n', 'false','0']
