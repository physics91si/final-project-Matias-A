import numpy as np
from constants import MINEFIELD_PARAM, MINEFIELD_SIZE
from logic_model import use_logic
from square_model import use

'''Keras model disabled due to problems with virtual env'''

TYPE = '5x5'
LOGIC_GEN = 2

def maxcoord(matrix):
    #returns the max coordinate of a 2D matrix
    xmaxs = np.amax(matrix, axis=1)
    maxx = np.argmax(xmaxs)
    ymaxs = np.amax(matrix, axis=0)
    maxy = np.argmax(ymaxs)
    return (maxx, maxy)

def eventhandler_ai(knowledge, prob_mine, flagged):
    if TYPE=='RANDOM':
        return 1, (np.random.randint(0,knowledge.shape[0]), np.random.randint(0,knowledge.shape[1]))
    if TYPE == '5x5':
        coord = use(knowledge, prob_mine)
        return 1,coord
    if TYPE=='LOGIC':
        return use_logic(knowledge, prob_mine, flagged, LOGIC_GEN)
    return 0,(0,0)
