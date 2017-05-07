from sklearn.metrics import jaccard_similarity_score

import pandas as pd
import numpy as np

pd.set_option('display.width', 1000)

def compute_jaccard(set_1, set_2):
    return len(set_1.intersection(set_2)) / float(len(set_1.union(set_2)))

def clean_data(d):
    return map(lambda x: x.lower(), d)

def lev_dist(s, t):
    d = [[0 for _ in range(len(s)+1)] for _ in range(len(t)+1)]

    for i in range(len(t)+1):
        d[i][0] = i
    for i in range(len(s)+1):
        d[0][i] = i

    d[0][0] = 0
    
    for r in range(1, len(t)+1):
        for c in range(1, len(s)+1):
            if s[c-1] == t[r-1]:
                d[r][c] = d[r-1][c-1]
            else:
                d[r][c] = min(d[r-1][c-1]+1, d[r-1][c]+1, d[r][c-1]+1)

    return d[len(t)][len(s)]

of = pd.read_csv('./of_airports.csv')
fd = pd.read_csv('./fd_airports.csv')

t1 = of.columns.values
t2 = fd.columns.values

res = [[None for _ in range(len(t2))] for _ in range(len(t1))]

for r, a1 in enumerate(t1):
    for c, a2 in enumerate(t2):
        min_len = min(len(a1), len(a2))
        attr1 = clean_data(a1[:min_len])
        attr2 = clean_data(a2[:min_len])
        res[r][c] = lev_dist(attr1, attr2)

print pd.DataFrame(res, t1, t2)
print

for i, r in enumerate(res):
    if min(r) > 0:
        continue
    print '%s => %s' % (t1[i], t2[r.index(min(r))])

res = [[None for _ in range(len(t2))] for _ in range(len(t1))]

print

for r, a1 in enumerate(t1):
    for c, a2 in enumerate(t2):
        res[r][c] = compute_jaccard(set(of[a1]), set(fd[a2]))

print pd.DataFrame(res, t1, t2)
print

for i, r in enumerate(res):
    if max(r) < 0.0024:
        continue
    print '%s => %s' % (t1[i], t2[r.index(max(r))])
