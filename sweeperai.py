import numpy as np
import gameplay
import gym

MINEFIELD_PARAM = [3]
MINEFIELD_SIZE = [30,16]
N = 1000
Q = np.random.randn(30*16, 2*30*16)
TYPE = 'RANDOM'

def evaluate(Q = Q, show=False):
    score = 0
    for i in range(N):
        newscore = gameplay.main(show = show, minefield_param = MINEFIELD_PARAM, Q = Q)
        if newscore == -1:
            score *= (float(N)/np.maximum(1,i))
            break
        score += newscore
    return float(score)/N

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
    print(evaluate(show=False))

def eventhandler_ai(Q, knowledge):
    # Q is (x*y, 2*x*y) numpy matrix
    if TYPE=='RANDOM':
        return 1, (np.random.randint(0,knowledge.shape[0]), np.random.randint(0,knowledge.shape[1]))
    guess = np.dot(Q, knowledge.flatten())
    guess = guess.reshape(knowledge.shape[0], knowledge.shape[1])
    coord = maxcoord(guess)
    return 1, coord

'''
weights = []
scores = []
best = np.zeros((30*16, 2*30*16))

for i in range(10000):
     weights.append(np.random.randn(30*16, 2*30*16))
     scores.append(evaluate(Q=weights[i]))
     if scores[i]==maxscore(scores):
         best = weights[i]
     if i%500 == 0:
         print(i)
print("done, max " + str(maxscore(scores)))
for i in range(10):
    print(evaluate(Q=best))
'''
