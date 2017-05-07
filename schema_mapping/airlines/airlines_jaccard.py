from sklearn.metrics import jaccard_similarity_score

import pandas as pd
import numpy as np

def compute_jaccard(set_1, set_2):
    return len(set_1.intersection(set_2)) / float(len(set_1.union(set_2))) 

of = pd.read_csv('./of_airlines.csv')
fd = pd.read_csv('./fd_airlines.csv')

t1 = of.columns.values
t2 = fd.columns.values

res = [[None for _ in range(len(t2))] for _ in range(len(t1))]

for r, a1 in enumerate(t1):
    for c, a2 in enumerate(t2):
        res[r][c] = compute_jaccard(set(of[a1]), set(fd[a2]))

print pd.DataFrame(res, t1, t2)
