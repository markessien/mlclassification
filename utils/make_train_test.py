
import os
import shutil

from utils.constants import image_extensions


def make_train_test(category_folder):

    if not os.path.isdir(category_folder):
        print("Input a folder")

        return

    # It is assumed that the inputted folder has been validated
    # to contain only just images. Basically, the folder should
    # have passed through @Munirat's code
    for folder_name, folders, files in os.walk(category_folder):

        # Create their paths. They'll be in the first level of the folder inputted
        training_folder = os.path.join(category_folder, '__training_set')
        test_folder = os.path.join(category_folder, '__test_set')

        # Actually create the folders
        os.mkdir(training_folder)  
        os.mkdir(test_folder)

        # Take 80% of the files in that directory
        for i in range(int(len(files)*0.8)): 
            # Check if they are valid images
            if files[i].endswith(image_extensions): 
                # And copy it to the training set folder
                shutil.copy(os.path.join(folder_name, files[i]), training_folder)

        # After copying to the training folder, then os.walk in the training folder. 
        # I'm using os.walk because the function is a generator,
        # and so we won't have a problem if the files are very 
        # many. Generators provide (yield) items as needed (once per time)
        # unlike lists which provide everything at once. Like always, 
        # any better solution should be implemented.
        # There was no need to create my own generator since python
        # already has os.walk inbuilt.

        # Also, note the naming system I used. The folder_name, folders
        # and files have an underscore before them. This is to 
        # differentiate them from the original ones in the category_folder
        for _folder_name, _folders, _files in os.walk(training_folder):
            # Loop through the files in the main category_folder
            # We want to get the remaining  20% of the files to
            # copy to the test set folder
            for file in files:
                # If any of the files is not in training folder
                if file not in _files:
                    # Then copy it to the test folder
                    shutil.copy(os.path.join(folder_name, file), test_folder)


        
        return





# make_train_test('/home/olumide/Desktop/Test')
