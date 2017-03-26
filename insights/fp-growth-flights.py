from fp_growth import find_frequent_itemsets

"""Notes:

* Depending on airports selected the number of found frequent sets can
  vary a lot. E.g. for a support of 50, HKG will have 27 while FRA
  will have 6781 frequent sets.

* Algorithm runs extemely slow if we do not remove duplicate flights
  WITHIN the transactions.

"""

transactions = []
with open("../datastore/results/flight_transactions") as f:
    for line in f:
        trans = line.split(",")
        trans = list(set(trans))                             # Remove duplicates
        trans = map(lambda x: set(x.split("->")), trans)     # Do not consider direction
        trans = map(lambda x: '-'.join(x), trans)

        if "SYD" in ''.join(trans):                          # Filter out one airport
            transactions.append(trans)

print("Process %s of transactions" % len(transactions))

# Obscure data science voodoo
min_sup = 30+len(transactions)/10
if min_sup > 130:
    min_sup = 130

# fire FP Growth mining
res = find_frequent_itemsets(transactions, min_sup, True)

i = 0
for r in res:
    freq_set = r[0]

    if len(freq_set) > 2:
        i += 1
        print(r)

print("Done\n")
print("%s frequent sets found with minimal support of %s in %s transactions" % (i, round(min_sup, 2), len(transactions)))

