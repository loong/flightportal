import pandas

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

def clean_data(d):
    return map(lambda x: x.lower(), d)

t1 = ['id', 'name', 'alias', 'iata', 'icao', 'callsign', 'country', 'active']
t2 = ['Name', 'URL', 'Country', 'IATA', 'Value', 'Label', 'ID']

res = [[None for _ in range(len(t2))] for _ in range(len(t1))]

for r, a1 in enumerate(t1):
    for c, a2 in enumerate(t2):
        res[r][c] = lev_dist(clean_data(a1), clean_data(a2))

print pandas.DataFrame(res, t1, t2)
