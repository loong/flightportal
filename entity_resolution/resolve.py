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

skylines = None
openlines = None

gold_file = open('gold_matches', 'w')
silver_file = open('silver_matches', 'w')
crap_file = open('crap_matches', 'w')

with open('uk_flight_delay_data', 'r') as f:
    skylines = f.readlines()
    skylines = map(lambda x: x[:-1], skylines)

with open('openflights_airlines', 'r') as f:
    openlines = f.readlines()
    openlines = map(lambda x: x[:-1], openlines)

def clean(s):
    s = s.lower()

    # Note: Order is important
    if len(s) > 8:
        s = s.replace('airlines', '')
        s = s.replace('airline', '')
        s = s.replace('aviation', '')
        s = s.replace('airways', '')

    return s
    
for sky in skylines:
    dists = [0 for _ in range(len(openlines))]
    
    for i, open in enumerate(openlines):
        clean_sky = clean(sky)
        clean_open = clean(open)
        min_length = min(len(clean_sky), len(clean_open))
        
        dist = lev_dist(clean_sky, clean_open)
        dists[i] = (dist, open)

    min_dist = min(dists, key=lambda x: x[0])

    candidates = filter(lambda x: x[0] == min_dist[0], dists)
    candidates = map(lambda x: x[1], candidates)

    print '%s, %s, %d' % (sky, candidates, min_dist[0])

    if min_dist[0] == 0:
        gold_file.write('%s, %s, %d\n' % (sky, candidates[0], min_dist[0]))
    elif min_dist[0] == 1 or len(candidates) == 1:
        silver_file.write('%s, %s, %d\n' % (sky, candidates, min_dist[0]))
    else:
        crap_file.write('%s, %s, %d\n' % (sky, candidates, min_dist[0]))
                        
