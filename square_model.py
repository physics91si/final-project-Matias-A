import numpy as np

from keras.layers import Dense
from keras.models import Sequential
from keras.models import model_from_json
from keras.callbacks import ProgbarLogger
import utils.randomboarddata as data

DATASIZE = 10000
MODE = 'USE'

nnmodel = None

'''
The model tries to predict the probability a given square has a mine.
It can be trained on random boards where configuration is known.
'''

if __name__ == "__main__":
    train_new()

elif MODE=='USE':
    json_file = open('model.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    nnmodel = model_from_json(loaded_model_json)
    nnmodel.load_weights("model.h5")


def train_new():
    X,Y = data.makeData(DATASIZE)
    X=X.reshape((X.shape[0],25))
    train(X,Y)

def train_old():
    X,Y = data.makeData(DATASIZE)
    X=X.reshape((X.shape[0],-1))

    json_file = open('model.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()

    global nnmodel
    nnmodel = model_from_json(loaded_model_json)
    nnmodel.load_weights("model.h5")
    nnmodel.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
    nnmodel.fit(X,Y, epochs=200, batch_size = 64, verbose=0)
    scores = nnmodel.evaluate(X,Y)
    print(scores)
    model_json = nnmodel.to_json()
    with open("model.json", "w") as json_file:
        json_file.write(model_json)
    nnmodel.save_weights("model.h5")
    print("Saved model to disk")


def model(X):
    model = Sequential()
    model.add(Dense(32, input_dim=X.shape[1], activation='relu'))
    model.add(Dense(16, activation='relu'))
    model.add(Dense(8, activation='relu'))
    model.add(Dense(8, activation='relu'))
    model.add(Dense(1, activation='sigmoid'))
    return model

def train(X, Y):
    nnmodel = model(X)
    nnmodel.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
    progbar = ProgbarLogger()
    nnmodel.fit(X,Y, epochs=500, batch_size = 64, verbose=0)
    scores = nnmodel.evaluate(X,Y)
    print(scores)
    model_json = nnmodel.to_json()
    with open("model.json", "w") as json_file:
        json_file.write(model_json)
    nnmodel.save_weights("model.h5")
    print("Saved model to disk")

def use(knowledge,prob_mine,nnmodel=nnmodel):
    '''
    Uses the NN model to predict the square with smallest probability of being a mine
    input: knowledge, array with "not guessed" as -1
    '''


    grid = np.zeros((knowledge.shape[0]*knowledge.shape[1],25))
    dictionary = {}
    n=0
    for i in range(knowledge.shape[0]):
        for j in range(knowledge.shape[1]):
            coord = (i,j)
            if knowledge[coord]!=-1:
                continue

            dictionary[n]=coord

            matrix = data.make5x5(knowledge, coord,prob_mine)
            grid[n,:] = matrix.reshape((1,25))
            n += 1


    probs = nnmodel.predict(grid[:n,:])
    best = probs.argmin()
    bestcoord = dictionary[best]
    return bestcoord
