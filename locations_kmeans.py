import json
import numpy as np
from sklearn import cluster

# Load data from file
with open('locations.json') as json_data:
    data = json.load(json_data)
    data_size = len(data["locations"])
print("# of locations %d" % data_size)

# Binning to reduce the data size
# Bin size roughly correspond to half a day worth of data
bin_size = 100
bin_total = data_size/bin_size + 1
locations = [(0,0)]*(bin_total)

for bin_number in xrange(bin_total):
    i, lat, lon = 0, 0, 0
    for i in xrange(bin_size):
        loc_number = bin_number*bin_size+i
        if loc_number >= data_size:
            break
        
        loc = data["locations"][loc_number]
        if "latitudeE7" in loc:
            lat, lon = lat+int(loc["latitudeE7"]), lon+int(loc["longitudeE7"])
            i += 1

    lat, lon = lat/i, lon/i
    locations[bin_number] = [lat, lon]
print("Reduced to %d bins" % bin_total)

# Use K-Mean clustering to get k hotspots
k = 20
kmeans = cluster.KMeans(n_clusters=k, n_jobs=-2) #use all but one cpu
data = np.array(locations, np.int32)
kmeans.fit(data)

points = []
for centroid in kmeans.cluster_centers_:
    points.append({
        "lat": centroid[0]*1e-7,
        "lng": centroid[1]*1e-7
    })

labels = []
for count in np.bincount(kmeans.labels_):
    labels.append(float(count)/len(data)*100)

result = []
for l, p in zip(labels, points):
    result.append({"position": p, "label": round(l,2)})
result.sort(key=lambda x: x["label"], reverse=True)

# print results
for r in result:
    print("{0} : {1}".format(r["label"], r["position"]))

print("Write results to res.json")
with open('res.json', 'w') as outfile:
    json.dump(result, outfile)
