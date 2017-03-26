import sys

from fp_growth import find_frequent_itemsets
from pprint import pprint

"""Notes:

* Depending on airports selected the number of found frequent sets can
  vary a lot. E.g. for a support of 50, HKG will have 27 while FRA
  will have 6781 frequent sets.

* Algorithm runs extemely slow if we do not remove duplicate flights
  WITHIN the transactions.

"""

if len(sys.argv) < 2:
    print("Please provide airport IATA code. e.g.")
    print("\n\tpython fp-growth-flights.py HKG\n")
    exit(-1)

airport = sys.argv[1]

transactions = []
with open("../datastore/results/flight_transactions") as f:
    for line in f:
        trans = line.split(",")
        trans = list(set(trans))                             # Remove duplicates
        # trans = filter(lambda x: airport in x, trans)
        trans = map(lambda x: set(x.split("->")), trans)     # Do not consider direction
        trans = map(lambda x: '-'.join(x), trans)
        if airport in ' '.join(trans):                       # Filter out one airport
            transactions.append(trans)

print("Process %s of transactions for %s" % (len(transactions), airport))

# Obscure data science voodoo
min_sup = 30+len(transactions)/10
if min_sup > 130:
    min_sup = 130

# fire FP Growth mining
res = find_frequent_itemsets(transactions, min_sup, True)

# filter and sort results
result = filter(lambda x: len(x[0]) > 2, res)                # only keep sets with at least 3 items
result = filter(lambda x: airport in ' '.join(x[0]), result) # final set must include airport
result.sort(key=lambda x: x[1], reverse=True)

pprint(result)

print("Done\n")
print("%s frequent sets found with minimal support of %s in %s transactions" % (len(result), round(min_sup, 2), len(transactions)))

