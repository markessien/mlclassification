import os
from utils import create_necessary_folders
from utils import process_folder
from keras.preprocessing.image import ImageDataGenerator

unprocessed_dir = 'training_images'
new_folders = ['train_data', 'validation_data']
subfolders = ['hotels','not-hotels']
create_necessary_folders(new_folders, subfolders)
for folder in new_folders:
    for sub in subfolders:
        source_folder = os.path.join(unprocessed_dir,sub)
        dest_folder = os.path.join(folder,sub)
        process_folder(source_folder, dest_folder)

train_data_folder = 'train_data'
validation_data_folder = 'validation_data'

batch_size = 16
target_size = (64,64)

# this is the augmentation configuration we will use for training
train_datagen = ImageDataGenerator(
        rescale=1./255,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True)

# this is the augmentation configuration we will use for testing:
# only rescaling
validation_datagen = ImageDataGenerator(rescale=1./255)

# this is a generator that will read pictures found in
# subfolers of 'data/train', and indefinitely generate
# batches of augmented image data
train_generator = train_datagen.flow_from_directory(
        train_data_folder,  # this is the target directory
        target_size=target_size,  # all images will be resized to 150x150
        batch_size=batch_size,
        class_mode='binary')  # since we use binary_crossentropy loss, we need binary labels

# this is a similar generator, for validation data
validation_generator = validation_datagen.flow_from_directory(
        validation_data_folder,
        target_size=target_size,
        batch_size=batch_size,
        class_mode='binary')
