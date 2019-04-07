# Python 3.6.7
# Ubuntu 18.04
import shutil
import os
import json
import sys
import argparse
import argparse,errno

file_name = 'classification_results.json'  # the file name
image_extensions = ('jpeg', 'png', 'jpg', 'tiff', 'gif')  # add others

# model argument can be substituted with a model of ours

def copyanything(src, dst):
    try:
        shutil.copytree(src, dst)
    except OSError as exc: # python >2.5
        if exc.errno == errno.ENOTDIR:
            shutil.copy(src, dst)
        else: raise

def processor(src, dest_1='',dest_2='', count=0):

    hotels = []  # list of file names that are hotels
    not_hotels = []  # list of file names that are not hotels
    i=0
    for folder_name, folders, files in os.walk(src):            
        # After each iteration in a folder,
        for each in files:
            if i<count:
                i=i+1
                copyanything(os.path.join(folder_name, each), dest_1)
            else:
                if i<count+1000:
                    i=i+1
                    copyanything(os.path.join(folder_name, each), dest_2)               
    return


def parse_args(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--count',
        type=int,
        help='',
    )
    parser.add_argument(
        'src',
        help='',
    )
    parser.add_argument(
        'dest_1',
        help='',
    )
    parser.add_argument(
        'dest_2',
        help='',
    )
    return parser.parse_args(argv[1:])


def main(argv=sys.argv):
    """ The main script """

    input_type = None
    args = parse_args(argv)
    src = args.src
    dest_1=args.dest_1
    dest_2=args.dest_2
    count=args.count
    
    # if it's not a folder that was supplied, check if it's a file
    if not os.path.isdir(src):
        if os.path.isfile(src):
            if src.split('.')[1].lower() not in image_extensions:
                print("Error: An image file is required. Try again\n")
                return
            input_type = 'file'
            # add logic before here to pass in the model we want to use in the predictor
            processor( src, dest_1, dest_2, count)
            return
        print('Error: Invalid path. Kindly supply a valid folder or image path\n')
        return

    input_type = 'folder'

    # add logic before here to pass in the model we want to use in the predictor
    processor( src,dest_1, dest_2, count)

    if input_type == 'folder':
        print(
            f"Done! The '{file_name}' file has been written to respective folders in {src}")


if __name__ == '__main__':
    main()