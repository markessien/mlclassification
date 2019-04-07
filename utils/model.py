import os
from .constants import model_default
from .constants import model_extension


def model_delete(model_file):
    if os.path.isdir(model_file):
        print("This is a directory. Input a file name")
        return
    elif os.path.isfile(model_file):
        if model_file.split('.')[1].lower()!=model_extension:
            print("Error: A model file is required. Try again\n")
            return
        if(model_file == model_default):
            print("Can't delete default model")
            return
        os.remove(model_file)
        print("{} has been deleted".format(model_file))
        return
    print('Error: Invalid path. Kindly supply a valid folder or image path\n')
    return



def parse_args(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'model_filename',
        help='The name of the model file',
    )
    return parser.parse_args(argv[1:])



def main(argv=sys.argv):
    """ The main script """

    args = parse_args(argv)
    model_file = args.model_filename

    model_delete(model_file)



if __name__ == '__main__':
    main()