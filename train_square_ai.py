import numpy as np
from ai_evaluate import evaluate
import square_model as mod

#mod.train_new()
for i in range(100):
    mod.train_old()
    #print(evaluate(show=False))
