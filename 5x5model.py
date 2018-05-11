import numpy as np
from keras.layers import Dense
from keras.models import Sequentialt

'''
The model tries to predict the probability a given square has a mine.
It can be trained on random boards where configuration is known.
'''



def model(X):
    model = Sequential()
    model.add(Dense(12, input_dim=X.shape[1]*X.shape[2], activation='relu'))
    model.add(Dense(8, activation='relu'))
    model.add(Dense(1, activation='sigmoid'))
    return model

def train(X, Y):
    '''
    Again, X 5x5 as above, now y is 1 or 0
    1 if mine, 0 if not mine
    '''
    pass
