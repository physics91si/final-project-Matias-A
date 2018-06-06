#!/Users/matias/tensorflow/bin/python3
'''Contains functions for evaluating the computer's performance'''

import numpy as np
import gameplay2
import sys
from constants import MINEFIELD_PARAM, MINEFIELD_SIZE

N_evaluate = 1000
showbool = False

if len(sys.argv)>1:
    showbool = bool(sys.argv[1])

def evaluate(show=False):
    score = 0
    won = 0
    scores = []
    for i in range(N_evaluate):
        newscore, won_bool = gameplay2.play(show = show, minefield_param = MINEFIELD_PARAM)
        scores.append(newscore)
        if newscore == -1:
            score *= (float(N_evaluate)/np.maximum(1,i))
            won *= (float(N_evaluate)/np.maximum(1,i))
            break
        if won_bool:
            won += 1
        score += newscore
        if i%10==0:

            sys.stdout.write("\r{}/{}".format(i,N_evaluate))
            sys.stdout.flush()

    np.savetxt('scores0.out.csv', scores, delimiter=',')
    sys.stdout.write("\r{}/{}\n".format(N_evaluate,N_evaluate))
    sys.stdout.flush()



    return (float(score)/N_evaluate, float(won)/N_evaluate)

def avgscore(l):
    s = 0
    for n in l:
        s+=n
    return float(s)/len(l)

def maxscore(l):
    m = 0
    for n in l:
        if n>m:
            m=n
    return m

if __name__=='__main__':
    out = evaluate(show=showbool)
    print("Average score: {}".format(out[0]))
    print("Percentage of games won: {}".format(out[1]))
