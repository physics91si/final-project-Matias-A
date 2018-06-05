#!/usr/bin/python3

import numpy as np


def certainmines(knowledge, coord):
    emptysqs = []
    minesaround = knowledge[coord]
    for k in range(-1,2):
        for l in range(-1,2):
            newx = k+coord[0]
            newy = l+coord[1]
            if newx<0 or newy<0 or newx>=knowledge.shape[0] or newy>=knowledge.shape[1]:
                continue
            if knowledge[newx,newy]==-1:
                emptysqs.append((newx,newy))
    if len(emptysqs)==minesaround:
        return emptysqs
    return []


def neighbormines(c,flagged,shape):
    i = 0
    for k in range(-1,2):
        for l in range(-1,2):
            newx = k+c[0]
            newy = l+c[1]
            if newx<0 or newy<0 or newx>=shape[0] or newy>=shape[1]:
                continue
            if (newx,newy) in flagged:
                i+=1
    return i

'''
def flaggedaround(coord, flagged):
    n = 0
    for k in range(-1,2):
        for l in range(-1,2):
            newx = k+coord[0]
            newy = l+coord[1]
            if newx<0 or newy<0 or newx>=knowledge.shape[0] or newy>=knowledge.shape[1]:
                continue
            if (newx,newy) in flagged:
                n+=1
    return n

def supposemine(coord, newknowledge, flagged):
    copy = np.copy(newknowledge)
    for k in range(-1,2):
        for l in range(-1,2):
            if k==0 and l==0:
                continue
            newx = k+coord[0]
            newy = l+coord[1]
            if newx<0 or newy<0 or newx>=newknowledge.shape[0] or newy>=newknowledge.shape[1]:
                continue
            if newknowledge[newx,newy]==-1:
                continue
            if newknowledge[newx,newy]==0:
                return False
            copy[newx,newy]-=1
    for k in range(-1,2):
        for l in range(-1,2):
            newx = k+coord[0]
            newy = l+coord[1]
            if newx<0 or newy<0 or newx>=newknowledge.shape[0] or newy>=newknowledge.shape[1]:
                continue
            if copy[newx,newy]==0:
                for x in range(-1,2):
                    for y in range(-1,2):
                        newx2 = x+newx
                        newy2 = y+newy
                        if copy[(newx,newy)]==-1
'''

def use_logic(knowledge, prob_mine, flagged, gen):
    guessed = []

    for i in range(knowledge.shape[0]):
        for j in range(knowledge.shape[1]):
            coord = (i,j)
            if knowledge[coord]>0:
                #Saves guessed coordinates
                guessed.append(coord)
                if neighbormines(coord,flagged,knowledge.shape)==knowledge[coord]:
                    for k in range(-1,2):
                        for l in range(-1,2):
                            newx = k+coord[0]
                            newy = l+coord[1]
                            if newx<0 or newy<0 or newx>=knowledge.shape[0] or newy>=knowledge.shape[1]:
                                continue
                            if knowledge[newx,newy]==-1 and (newx,newy) not in flagged:
                                return 1,(newx,newy)

    mines = np.zeros(knowledge.shape)
    '''Flags 100% sure mines'''

    for c in guessed:
        cmines = certainmines(knowledge, c)
        for m in cmines:
            if m not in flagged:
                return 3, m
    '''
    if gen > 2:
        newknowledge = np.copy(knowledge)
        for c in guessed:
            newknowledge[c]-=flaggedaround(c, flagged)
        for c in guessed:
            for k in range(-1,2):
                for l in range(-1,2):
                    newx = k+c[0]
                    newy = l+c[1]
                    if newx<0 or newy<0 or newx>=knowledge.shape[0] or newy>=knowledge.shape[1]:
                        continue
                    if (newx,newy) in guessed:
                        continue
                    works = supposemine((newx,newy),newknowledge, flagged)
    '''

    if gen > 0:
        '''If doesn't find anything better, chooses a corner'''
        for i in np.random.permutation(2):
            for j in np.random.permutation(2):
                c = (i*(knowledge.shape[0]-1),j*(knowledge.shape[1]-1))
                if knowledge[c]==-1 and c not in flagged:
                    return 1,c
    '''Or an edge'''
    if gen > 1:
        # Chooses axis
        for a in np.random.permutation(2):
            axis0 = a
            axis1 = (a+1)%2
            # Chooses side
            for s in np.random.permutation(2):
                coord = [0,0]
                coord[axis0] = s*(knowledge.shape[axis0]-1)
                for i in np.random.permutation(knowledge.shape[axis1]):
                    coord[axis1] = i
                    c = tuple(coord)
                    if c not in flagged and knowledge[c]==-1:
                        return 1, c

    '''Or a random square'''
    for i in np.random.permutation(knowledge.shape[0]):
        for j in np.random.permutation(knowledge.shape[1]):
            coord = (i,j)
            if coord not in flagged and knowledge[coord]==-1:
                return 1, coord
