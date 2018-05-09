#!/usr/bin/python3
import numpy as np

class Minefield:
    '''
    Initializes a minefield, either with custom size and mines (x,y,mines), or one of the 3 standard settings (1,2 or 3; from easy to hard)
    Has the following attributes:
    mines: x*y np-array with 1s at mines and 0s elsewhere
    neighbors: x*y np-array, -1 at mines, otherwise the number of neighbor mines
    guess(x,y): guesses a square, returns the number from neighbors
    get_size(): returns x,y
    '''
    def __init__(self, *args):

        if len(args)==1:
            level = args[0]
            if level==1:
                args = (9,9,10)
            elif level==2:
                args = (16,16,40)
            elif level==3:
                args = (30,16,99)

        #Unpacks arguments

        x=args[0]
        y=args[1]
        mines=args[2]
        self.mines = np.zeros((x,y), dtype=int)
        if mines<0:
            raise Exception("Negative number of mines")
        if mines>x*y:
            raise Exception("Too many mines")
        for i in range(mines):

            #Fills the minefield
            while True:
                xmine=np.random.randint(0,x)
                ymine=np.random.randint(0,y)
                if self.mines[xmine,ymine]==0:
                    break
            self.mines[xmine,ymine]=1

        #initializes neighbors with mines as -1
        self.neighbors=-self.mines
        for i in range(x):
            for j in range(y):
                # loops over all the squares on the mine field
                if self.mines[i,j]==1:
                    #selects all the mines
                    for k in range(-1,2):
                        for l in range(-1,2):
                            #loops over the 9 square block around the mine
                            if i+k>=0 and i+k<x and j+l>=0 and j+l<y:
                                #selects only squares inside the grid
                                if self.neighbors[i+k,j+l]!=-1:
                                    #makes sure the square is not a mine
                                    self.neighbors[i+k,j+l]+=1

    def __str__(self):
        return "Mines: \n" + np.array2string(self.mines) + "\nNeighbors: \n"+ np.array2string(self.neighbors)

    def guess(self, x,y):
        return self.neighbors[x,y]

    def get_size(self):
        return self.mines.shape

    def get_mines(self):
        return np.sum(self.mines)
