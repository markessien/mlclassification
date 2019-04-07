
import os
from pathlib import Path

model_default = 'default_model.h5'

root_dir = Path(__file__).parents[1] # The root directory (mlclassification)
model_dir = os.path.join(root_dir, "models") # the models directory

model_extension = "h5"
