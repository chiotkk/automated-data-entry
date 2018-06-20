import numpy as np
from keras.datasets import mnist
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.utils import np_utils
from PIL import Image


# Fixed seed for reproducibility
seed = 7
np.random.seed(seed)


# Define network model
(X_train, y_train), (X_test, y_test) = mnist.load_data()

num_pixels = X_train.shape[1] * X_train.shape[2]
X_train = X_train.reshape(X_train.shape[0], num_pixels).astype('float32')
X_test = X_test.reshape(X_test.shape[0], num_pixels).astype('float32')

X_train = X_train/255
X_test = X_test/255

y_train = np_utils.to_categorical(y_train)
y_test = np_utils.to_categorical(y_test)
num_classes = y_test.shape[1]


def baseline_model():
    model = Sequential()
    model.add(Dense(num_pixels, input_dim=num_pixels, kernel_initializer='normal', activation='relu'))
    model.add(Dense(num_classes, kernel_initializer='normal', activation='softmax'))

    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    return model


def predict(model, image_name):

    img = Image.open(image_name)
    arr = np.array(img)

    if (np.sum(arr) == 0):
        return 0
    
    shape = arr.shape
    flat_arr = arr.ravel()
    vector = np.matrix(flat_arr)
    result = model.predict(vector)
    result = np.argmax(result, axis=1)

    return result[0]


def train():
    # Instantiate network model
    model = baseline_model()
    model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=10, batch_size=200, verbose=2)

    scores = model.evaluate(X_test, y_test, verbose=0)
    print("Baseline error: %.2f%%" % (100-scores[1]*100))

    return model


def get_serial(model):
    serial = ''
    for i in range(6):
        serial += str(predict(model, r'processed_images\s{}.png'.format(i+1)))
    return serial


def get_date(model):
    date = ''
    for i in range(6):
        date += str(predict(model, r'processed_images\d{}.png'.format(i+1)))
    return date


def get_data(model):
    values = []
    unit_check = []
    for i in range(18):
        qty = ''
        for j in range(12):
            qty += str(predict(model, r'processed_images\{}-{}.png'.format(i+1, j+1)))
            if (j == 2) or (j == 6):
                if (j ==2):
                    values.append(qty)
                else:
                    unit_check.append(qty)
                qty = ''
        qty = qty[:-2] + '.' + qty[-2:]
        values.append(qty)
            
    return values, unit_check
    
