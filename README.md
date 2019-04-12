# Image Classification of Hotels and Non-Hotels

This project is carried out for the purpose of building a machine learning model for classifying images of Hotes from Non-hotels

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Project Structure

```
.
├── datasets
│   ├── test_set
│   │   ├── hotels
│   │   └── not-hotels
│   │            
│   │             
│   └── training_set
├       ├── hotels
├       └── not-hotels
├── model
│   └── default_model.h5
│   
│   
├── utils
├── requirements.txt
├── app.py
└── README.md
```

### Prerequisites

Python distribution

```
Anaconda
```

### Installing

Install Anaconda python distribution on your system

Create a virtual environment called env.

```
python -m venv env
```

Activate the virtual environment

```
LINUX/Mac: source env/bin/activate

Windows: env\Scripts\activate
```

Upgrade to the latest pip

```
pip install --upgrade pip
```

Install dependencies using requirements file

```
pip install -r requirements.txt
``` 
**Note: Your virtual environment must always be activated before running any command**

## Deployment

Start app (Make sure to enter a valid path to a file or a folder)


Example of valid commands

```
python app.py predict --path kimono-1986491_640.jpg
python app.py predict --path predict
```

### Train App

Make sure you have a dataset folder with the below structure in the root folder of the app

A trained model weight file can be found [here](https://drive.google.com/drive/folders/1rYweIKMNjQiKC-D92BPEcK7CSPd_jDPb?usp=sharing), download and put it in the models folder.

Download and extract this [file](https://drive.google.com/file/d/15ExWHHPnzdqzQDM7ROxBdwohbxa5b_Lx/view?usp=sharing) to the root folder of the project or you can train your own model by providing a dataset folder in the root folder of the project with  below structure.

```
.
├── datasets
│   ├── test_set
│   │   ├── valid_case
│   │   └── not_valid_case
│   │            
│   │             
│   └── training_set
├       ├── valid_case
├       └── not_valid_case
```



### APIs

This are command options in full:

```
A command line utility for image classification.
-----------------------------------------------
These are common commands for this app.

positional arguments:
  app_action            This can either be predict, train, retrieve_models or
                        delete

optional arguments:
  -h, --help            show this help message and exit
  -path PATH, --path PATH
                        A path to a folder or image e.g foo or foobar.jpg
  -grpA GRPA, --grpA GRPA
                        A group A folder path e.g hotels
  -grpB GRPB, --grpB GRPB
                        A group B folder path e.g not-hotels
  -model MODEL, --model MODEL
                        Selects a model to be used
  -gen_name GEN_NAME, --gen_name GEN_NAME
                        A boolean to generate model name e.g yes or no
```
Below is specifics

**Retrieve Models:**

```
python app.py retrieve_models
```

**Delete Model:**

```
python app.py delete -model modelname
``` 

or:

```
python app.py delete --model modelname
```

**Train Model with custom dataset and model:**

```
python app.py train --grpA path/to/groupA --grpB path/to/groupB --model cat_dogmodel
```

or:

```
python app.py train -grpA path/to/groupA -grpB path/to/groupB -model cat_dogmodel
```

**Train with default dataset and model:**

If the default model already exists, delete it before proceeding

```
python app.py train
```

**Classification with default model:**

with image file:

```
python app.py predict --path /path/to/image.png
```

with folder:

```
python app.py predict --path /path/to/folder
```

or:

with image file:

```
python app.py predict -path /path/to/image.png
```

with folder:

```
python app.py predict -path /path/to/folder
```


**Classification with custom model:**

```
python app.py predict --path /Users/src/assets/images/bg.png --model modelname
```

or:

```
python app.py predict -path /Users/src/assets/images/bg.png -model modelname
```

## Built With

* [Anaconda](https://www.anaconda.com/distribution/) - The python distribution used
* [VS Code](https://code.visualstudio.com/) - The IDE used

## Documentation

Read documentation [here](https://docs.google.com/document/d/1rmpzDJTY0VO4IIhxTE0HqCEoa4yUMz3GCE-KlVNshTY/edit?usp=sharing)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE.md) file for details

## Acknowledgments

* Hat tip to anyone whose code was used
* Inspiration
* etc
