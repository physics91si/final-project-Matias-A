# import common libraries
import numpy as np

import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

#import files from parent folder
from minefield import Minefield
from sweeperai import MINEFIELD_PARAM

N = 1000

def random():
    field = Minefield(MINEFIELD_PARAM)
    shape = field.get_size()
    return field, shape

def makeData():
    X = np.zeros((N,5,5))
    Y = np.zeros((N,1))
    for i in range(N):
        field, shape = random()

        coord = (np.random.randint(0,shape[0]),np.random.randint(0,shape[1]))
        for j in range(-2,3):
            for k in range(-2,3):
                outbounds = j+coord[0]<0 or k+coord[1]<0 or j+coord[0]>=shape[0] or k+coord[1]>=shape[1]

                if outbounds:
                    print(str(j+coord[0]) + str(k+coord[1]))
