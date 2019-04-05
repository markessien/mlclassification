# mlclassification

Image Classification of Hotels and Non-Hotels
This project is carried out for the purpose of building a machine learning model for classifying images of Hotels and Non-hotels

Full process documentation can be found at https://docs.google.com/document/d/1rmpzDJTY0VO4IIhxTE0HqCEoa4yUMz3GCE-KlVNshTY/edit?usp=sharing

#Getting Started
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

#Prerequisites
1.Anaconda (Install Anaconda python distribution 3.7 on your system)

#Install VENV.. make sure to do this first
pip3 install requirements.txt

#If there is an app folder skip this step
 python3 -m venv app

#activate  VENV
LINUX/Mac: source app/bin/activate
Windows: app\Scripts\activate.bat

#Install dependencies in VENV
pip3 install -r  env/requirements.txt

GETTING STARTED
#Start app (Make sure to enter a valid path to a file or a folder)
python3 app.py

#Example of valid path

File path: ./predict/hotel/kimono-1986491_640.jpg

Folder path: ./predict

#Train app (Make sure to enter absolute path)
python3 train_model.py

License
This project is licensed under the MIT License - see the LICENSE.md file for details

Acknowledgments
Hat tip to anyone whose code was used
Inspiration
etc
