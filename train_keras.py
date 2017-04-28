# Build a keras neural network and train it

import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D
from keras import optimizers
from keras import backend as K
from utils import Screenshot

# Global variable
OUT_SHAPE = 5
INPUT_SHAPE = (Screenshot.IMG_H, Screenshot.IMG_W, Screenshot.IMG_D)

def customized_loss(y_true, y_pred, loss='euclidean'):
    # Simply a mean squared error that penalizes large joystick summed values
    if loss == 'L2':
        L2_norm_cost = 0.001
        val = K.mean(K.square((y_pred - y_true)), axis=-1) \
                    + K.sum(K.square(y_pred), axis=-1)/2 * L2_norm_cost
    # euclidean distance loss
    elif loss == 'euclidean':
        val = K.sqrt(K.sum(K.square(y_pred-y_true), axis=-1))
    return val

def creation_model(keep_prob = 0.8):
    # create model
    model = Sequential()

    # NVIDIA's model
    model.add(Conv2D(24, kernel_size=(5, 5), strides=(2, 2), activation='relu', input_shape= INPUT_SHAPE))
    model.add(Conv2D(36, kernel_size=(5, 5), strides=(2, 2), activation='relu'))
    model.add(Conv2D(48, kernel_size=(5, 5), strides=(2, 2), activation='relu'))
    model.add(Conv2D(64, kernel_size=(3, 3), activation='relu'))
    model.add(Conv2D(64, kernel_size=(3, 3), activation='relu'))
    model.add(Flatten())
    model.add(Dense(1164, activation='relu'))
    drop_out = 1 - keep_prob
    model.add(Dropout(drop_out))
    model.add(Dense(100, activation='relu'))
    model.add(Dropout(drop_out))
    model.add(Dense(50, activation='relu'))
    model.add(Dropout(drop_out))
    model.add(Dense(10, activation='relu'))
    model.add(Dropout(drop_out))
    model.add(Dense(OUT_SHAPE, activation='softsign'))

    return model


if __name__ == '__main__':
    # Load Training Data
    x_train = np.load("data/X.npy")
    y_train = np.load("data/y.npy")

    # Set none important second parameter to 0, or remove from fitting procedure
    # y_train[:, 1] = 0

    print(x_train.shape[0], 'train samples')

    # Training loop variables
    epochs = 100
    batch_size = 50

    # also possible to randomly shuffle images for training
    '''
    numbers = np.arange(x_train.shape[0])
    shuffle = np.random.choice(numbers, size=x_train.shape[0], replace=False)
    x_train = x_train[shuffle]
    y_train = y_train[shuffle]
    '''

    model = creation_model()
    model.compile(loss=customized_loss, optimizer=optimizers.adam())
    # fit (train) model; if random shuffle images was selected can also split part of the training data as validation
    model.fit(x_train, y_train, batch_size=batch_size, epochs=epochs)#, validation_split=0.1)

    # save whole model or only save weights and load mode from this file
    # model.save('model.h5')
    model.save_weights('model_weights.h5')
