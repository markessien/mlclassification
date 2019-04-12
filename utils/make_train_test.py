import sys
import os
import shutil
import math
import subprocess
from .constants import image_extensions
from .constants import root_dir

def copyWithSubprocess(cmd):
    DEVNULL = open(os.devnull, 'wb')        
    subprocess.Popen(cmd, stdout=DEVNULL, stderr=subprocess.STDOUT)



def make_train_test(groupa, groupb):
    
    if not (os.path.isdir(groupa) and os.path.isdir(groupb)):
        print("Input a folder")
        sys.stdout.flush()
        return
    #Make new directory at root
    new_dir = os.path.join(root_dir,'new_datasets')
    if os.path.isdir(new_dir):
        shutil.rmtree(new_dir)
    os.mkdir(new_dir)

    #make training_set and test_set directories inside new_dir
    training_set = os.path.join(new_dir,'training_sets')
    os.mkdir(training_set)
    test_set = os.path.join(new_dir,'test_sets')
    os.mkdir(test_set)
    
    #Create group A folder inside training set folder e.g hotel
    groupA_folder_train = os.path.join(training_set,os.path.basename(groupa))
    os.mkdir(groupA_folder_train)
    #Create group B folder inside training set folder e.g not-hotel
    groupB_folder_train = os.path.join(training_set,os.path.basename(groupb))
    os.mkdir(groupB_folder_train)

    #Create group A folder inside test set folder e.g hotel
    groupA_folder_test = os.path.join(test_set,os.path.basename(groupa))
    os.mkdir(groupA_folder_test)
    #Create group B folder inside test set folder e.g hotel
    groupB_folder_test = os.path.join(test_set,os.path.basename(groupb))
    os.mkdir(groupB_folder_test)
    
    #Now we have the structure new_datasets/training_set/groupa, new_datasets/training_set/groupb
    # And new_datasets/test_set/groupa, new_datasets/test_set/groupa

    #Copy folders content respectively
    #Copy whole to training set
    
    for file in os.listdir(groupa):
        if file.endswith(image_extensions):
            copyWithSubprocess(['cp',os.path.join(groupa,file), groupA_folder_train])
    for file in os.listdir(groupb):
        if file.endswith(image_extensions):
            copyWithSubprocess(['cp',os.path.join(groupb,file), groupB_folder_train])
    
    # Copy 20% to test_set
   
    total = math.ceil(len(os.listdir(groupa))*0.2)
    
    for file in os.listdir(groupa)[:total]:
        if file.endswith(image_extensions):
            copyWithSubprocess(['cp',os.path.join(groupa,file), groupA_folder_test])
               
    
    total = math.ceil(len(os.listdir(groupb))*0.2)
    for file in os.listdir(groupb)[:total]:
        if file.endswith(image_extensions):
            copyWithSubprocess(['cp',os.path.join(groupb,file), groupB_folder_test])

    return dict(training_set = training_set,test_set=test_set)
                

if __name__ == '__main__':
    # A Test
    make_train_test('./datasets/training_set/hotels','./datasets/training_set/not-hotels')
