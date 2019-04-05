# Image Classification of Hotels and Non-Hotels

This project is carried out for the purpose of building a machine learning model for classifying images of Hotes from Non-hotels

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

Python distribution

```
Anaconda
```

### Installing

Install Anaconda python distribution on your system

Use the pip package to create virtual environment (VENV) using the requirements file

```
pip3 install requirements.txt
```

If there is an app folder skip this step

```
python3 -m venv app
```

Activate the virtual environment (VENV)

```
LINUX/Mac: source app/bin/activate

Windows: app\Scripts\activate.bat
```

Install dependencies in VENV using requirements file

```
pip3 install -r  env/requirements.txt
``` 

## Deployment

Start app (Make sure to enter a valid path to a file or a folder)

```
python3 app.py filepath
```

Example of valid path

```
python3 app.py ./kimono-1986491_640.jpg
python3 app.py ./predict
```

### Train App

```
python3 train_model.py
```

## Built With

* [Anaconda](https://www.anaconda.com/distribution/) - The python distribution used
* [VS Code](https://code.visualstudio.com/) - The IDE used

## Documentation

Read documentation [here](https://docs.google.com/document/d/1rmpzDJTY0VO4IIhxTE0HqCEoa4yUMz3GCE-KlVNshTY/edit?usp=sharing)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Hat tip to anyone whose code was used
* Inspiration
* etc
