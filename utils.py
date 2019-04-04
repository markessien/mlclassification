import os
import shutil



def is_image(file):
    """Checks if file is an image"""
    root, ext = os.path.splitext(file)
    if ext not in ['.jpg', '.jpe', '.jpeg', '.png']:
        return False
    return True

def create_necessary_folders(folders, subfolders):
    for folder in folders:
        if not os.path.exists(folder):
            os.mkdir(folder)
            # create hotels and not-hotels subfolder
            for sub in subfolders:
                os.mkdir(os.path.join(folder,sub))
        
    return folders


def process_folder(source_folder, dest_folder):
    """Processes the images in a folder"""
    for file in os.listdir(source_folder):
        if is_image(file):
            #Avoid duplicate
            if not os.path.exists(os.path.join(dest_folder,file)):
                #copy
                shutil.copy(os.path.join(source_folder,file),dest_folder)
           