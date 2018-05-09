#!/usr/bin/python3

import numpy as np
import pygame
from minefield import Minefield
from sweeperai import eventhandler_ai, MINEFIELD_PARAM

BLACK    = (   0,   0,   0)
GREY     = ( 127, 127, 127)
DARK_GREY= (  63,  63,  63)
WHITE    = ( 255, 255, 255)
GREEN    = (   0, 255,   0)
RED      = ( 255,   0,   0)
SKY_BLUE = ( 117, 187, 253)
LINE_WIDTH = 1
SQ_SPACING = .05
SIZE = (1200, 800)
TOP = 50
SCOREFONT = 20
COMPUTERSPEED = 4

def square_size_position(field, screen, emptyspace = 0.1):
    '''
    parameters: field size (squares) and screen size (pixels), both (x,y)
    empty space as a percentage (default: 10%)
    returns: int size, nparray (x,y) where (x,y) is the position of the left upper corner
    '''
    field_ratio = float(field[0])/float(field[1]) # x/y
    screen_ratio = float(screen[0])/float(screen[1]-TOP)
    if screen_ratio < field_ratio: ## limiting coordinate is x
        size = int((1-emptyspace)*float(screen[0])/field[0])
        x = int(emptyspace * screen[0]/2)
        y = int((screen[1]-field[1]*size)/2)+TOP
        return size, (x,y)
    size = int((1-emptyspace)*float(screen[1]-TOP)/field[1])
    y = int(emptyspace * screen[1]/2)+TOP
    x = int((screen[0]-field[0]*size)/2)
    return size, np.asarray((x,y))


def eventhandler_human(rectdict):
    '''Returns a guess: (type, (x,y))'''
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return -1, (0,0)
        if event.type == pygame.MOUSEBUTTONDOWN:
            click_position = event.pos
            click_type = event.button #left = 1, right = 3
            for coord, rect in rectdict.items():
                if rect.collidepoint(click_position):
                    return click_type, coord
    return 0, (0,0)
def maxcoord(matrix):
    #returns the max coordinate of a 2D matrix
    xmaxs = np.amax(matrix, axis=1)
    maxx = np.argmax(xmaxs)
    ymaxs = np.amax(matrix, axis=0)
    maxy = np.argmax(ymaxs)
    return (maxx, maxy)




def printscreen(screen, flagged, rectangles_todraw, numbers_todraw, rectdict, mines, guessed):
    screen.fill(WHITE)

    text = pygame.font.Font(None, SCOREFONT)
    diff = mines-len(flagged)
    image = text.render("Mines left: " + str(np.maximum(0,diff)) + "     Score: " + str(len(guessed)), True, DARK_GREY)
    screen.blit(image, (SIZE[0]/2-image.get_width()/2, TOP/2-image.get_height()/2))

    for coord in flagged:
        rect = rectdict[coord]
        pygame.draw.rect(screen, GREY, rect, 0)
    for rect in rectangles_todraw:
        pygame.draw.rect(*rect)
    for number in numbers_todraw:
        screen.blit(*number)
    pygame.display.update()



def main(human=False, show=True, Q = 0, minefield_param = MINEFIELD_PARAM):
    #by default runs as computer version
    #initializes screen if "show" chosen
    if show:
        pygame.init
        pygame.font.init()
        screen = pygame.display.set_mode(SIZE)
        pygame.display.set_caption("Blatant Minesweeper Copy")

        clock=pygame.time.Clock()


    field = Minefield(*minefield_param)
    shape = field.get_size()  # shape of the minefield
    # prepares the rectangles
    if show:
        square_size, square_pos = square_size_position(shape, SIZE)
        rectdict = {}
        rectangles_todraw = []
        for i in range(shape[0]):
            for j in range(shape[1]):
                pos = square_pos + (np.asarray((i,j))*square_size)
                rectangle = pygame.Rect(pos[0], pos[1], int(square_size*(1-SQ_SPACING)), int(square_size*(1-SQ_SPACING)))
                rectdict[(i,j)]=rectangle
                rectangles_todraw.append((screen, BLACK, rectangle, LINE_WIDTH))


    done = False
    lost = False
    won = False
    update = False
    flagged = [] # list of flagged coordinates
    guessed = [] # list of guessed coordinates
    numbers_todraw = []
    mines = field.get_mines()
    squares = shape[0]*shape[1]

    knowledge = np.zeros((*shape, 2))
    knowledge[:,:,1] -=1
    '''knowledge is the array that is fed into the AI:
    it contains the grid twice, first just 0,1
    then -1, value
    -> initially it's just 0s and -1s.
    '''

    if show:
        printscreen(screen, flagged, rectangles_todraw, numbers_todraw, rectdict, mines, guessed)
    while not done:
        #when computer, check if user wants to quit
        if show and not human:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True

        #get guess, either for human or computer
        if human:
            guesstype, guesscoord = eventhandler_human(rectdict)
            if guesstype == -1:
                done = True
        else:
            guesstype, guesscoord = eventhandler_ai(Q, knowledge)
            #guesstype, guesscoord = 1, (np.random.randint(0,shape[0]), np.random.randint(0,shape[1]))

        # process left click
        if guesstype == 1:
            if guesscoord in guessed:
                if not human:
                    lost = True
                    done = True
                    break
                continue
            toprocess = [guesscoord]
            while True:
                if len(toprocess) != 0:
                    guesscoord = toprocess[0]
                    toprocess.remove(guesscoord)
                knowledge[guesscoord,0]=1
                if guesscoord in flagged:
                    flagged.remove(guesscoord)

                guessed.append(guesscoord)
                value = field.guess(*guesscoord)
                knowledge[guesscoord, 1] = value
                if value == -1:
                    lost = True
                    done = True
                    if show:
                        rect = rectdict[guesscoord]
                        rectangles_todraw.append((screen, BLACK, rect, 0))
                        update = True
                    break

                elif show:
                    rect = rectdict[guesscoord]
                    number = pygame.font.Font(None, int(square_size*(1-SQ_SPACING))-LINE_WIDTH)
                    image = number.render(str(value), True, BLACK)
                    numbers_todraw.append((image, (rect.center[0]+1-image.get_width()/2, rect.center[1]+1-image.get_height()/2)))
                    update = True

                if value==0:
                    for i in range(-1,2):
                        for j in range(-1,2):
                            newx = i+guesscoord[0]
                            newy = j+guesscoord[1]
                            if newx<0 or newy<0 or newx>=shape[0] or newy>=shape[1]:
                                continue
                            if (newx, newy) not in guessed and (newx, newy) not in toprocess:
                                toprocess.append((newx,newy))
                if len(toprocess)==0:
                    break

        # process right click
        elif guesstype == 3:
            if guesscoord in flagged:
                flagged.remove(guesscoord)
                update = True
            elif guesscoord not in guessed:
                flagged.append(guesscoord)
                update = True

        # updates the screen
        if update and show:
            printscreen(screen, flagged, rectangles_todraw, numbers_todraw, rectdict, mines, guessed)
            update = False

        #checks if won
        if squares-len(guessed)==mines:
            won = True
            done = True

        # ticks
        if human:
            clock.tick(60)
        elif show:
            clock.tick(COMPUTERSPEED)

    #print messages for winning and losing
    if lost and show:
        done = False
        print("You lost!")
        text = pygame.font.Font(None, int(.3*SIZE[1]))
        image = text.render("You lost!", True, SKY_BLUE)
        screen.blit(image, (SIZE[0]/2-image.get_width()/2, SIZE[1]/2-image.get_height()/2))
        pygame.display.flip()
    elif won and show:
        done = False
        print("You won!")
        text = pygame.font.Font(None, int(.3*SIZE[1]))
        image = text.render("You won!", True, SKY_BLUE)
        screen.blit(image, (SIZE[0]/2-image.get_width()/2, SIZE[1]/2-image.get_height()/2))
        pygame.display.flip()

    # if human player, doesn't automatically close the window
    while not done and human:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

    if not human and not lost and not won:
        return -1

    # returns the score
    if not human:
        return len(guessed)



if __name__ == "__main__":
    main(human=True)
