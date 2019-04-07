from keras.models import load_model
from sklearn.metrics import confusion_matrix
import numpy as np
def evaluate(model):
	load = load_model(model)
	predict_test = load.predict_generator(test_generator, step=1, verbose=0)
	predict =  np.argmax(predict_test, axis=1)
	conf_matrix = confusion_matrix(test_generator.classes, predict)
	return conf_matrix
evaluate('model.h5')