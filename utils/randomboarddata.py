# import common libraries
import numpy as np

import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

#import files from parent folder
from minefield import Minefield
from constants import MINEFIELD_PARAM


def make5x5(guesses, coord, prob_mine):
    shape = guesses.shape
    arr = np.full((5,5),-1)
    for i in range(-2,3):
        for j in range(-2,3):
            newx = i+coord[0]
            newy = j+coord[1]
            if newx<0 or newy<0 or newx>=shape[0] or newy>=shape[1]:
                arr[i+2,j+2]=-1
            else:
                arr[i+2,j+2] = guesses[newx,newy]
    arr[2,2]=prob_mine
    return arr

def random():
    field = Minefield(*MINEFIELD_PARAM)
    shape = field.get_size()
    return field, shape

def makeData(N=10):
    X = np.zeros((N,5,5))
    Y = np.zeros((N,1))
    for i in range(N):
        if (i)%50==0:
            sys.stdout.write("\rGenerating dataset: {}/{}".format(i,N))
            sys.stdout.flush()
        field, shape = random()
        prob = 1-np.random.power(1)
        numberguessed = int(prob*(shape[0]*shape[1]-field.get_mines()))
        toCheck = []
        guesses = np.full(shape,-1)
        guessed = []
        while True:
            '''Generates a minefield'''
            if len(toCheck)!=0:
                coord = toCheck[0]
                toCheck.remove(coord)
            else:
                coord = (np.random.randint(0,shape[0]),np.random.randint(0,shape[1]))
                if coord in guessed:
                    continue


            value = field.guess(coord[0],coord[1])
            if value == -1:
                continue
            guessed.append(coord)
            guesses[coord]=value
            if value == 0:
                for k in range(-1,2):
                        for l in range(-1,2):
                            newx = k+coord[0]
                            newy = l+coord[1]
                            if newx<0 or newy<0 or newx>=shape[0] or newy>=shape[1]:
                                continue
                            if (newx, newy) not in guessed and (newx, newy) not in toCheck:
                                toCheck.append((newx,newy))
            if len(guessed)>=numberguessed and len(toCheck)==0:
                break

        '''Chooses a random square on the minefield'''
        coord = (np.random.randint(0,shape[0]),np.random.randint(0,shape[1]))
        while coord in guessed:
            coord = (np.random.randint(0,shape[0]),np.random.randint(0,shape[1]))
        '''Makes a 5x5 square'''
        #prob_mine is number of mines divided by open squares
        prob_mine = float(field.get_mines())/(shape[0]*shape[1]-numberguessed)
        X[i,:,:] = make5x5(guesses, coord, prob_mine)
        yval = field.guess(coord[0],coord[1])
        if yval == -1:
            Y[i,0]=1
        else:
            Y[i,0]=0

    sys.stdout.write("\rGenerating dataset: {}/{}\n".format(N,N))
    sys.stdout.flush()
    return X,Y

if __name__ == "__main__":
    X,Y = makeData()
    print(X[0,:,:])
    print(Y[0:10])
