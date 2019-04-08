
#%%
from keras.models import load_model
from keras.preprocessing import image
from keras.preprocessing.image import load_img, img_to_array
import numpy as np

def prepImage(image):
    test_image = load_img(image, target_size=(64, 64))
    test_image = img_to_array(test_image)
    test_image = np.expand_dims(test_image, axis=0)
            
    return test_image

def validation_metrics (image, y):
    model = load_model('models/default_model.h5')
    array = prepImage(image)
    y = np.array(y)
    y = y.reshape(-1,1)
    metrics = model.evaluate(array, y)
    return model.metrics_names, metrics
    

#testing with an image
validation_metrics('bed-2581092_640.jpg', 1)

#%%  

