from sklearn.metrics.pairwise import pairwise_distances
import numpy as np
import kmedoids
import json

# Load data from file
print("Reading from json file")
with open('locations.json') as json_data:
    data = json.load(json_data)
    data_size = len(data["locations"])
print("Number of locations found: %d" % data_size)

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

# Use K-Medoids clustering to get k hotspots
k = 40
D = pairwise_distances(locations, metric='euclidean')
medoids, C = kmedoids.kMedoids(D, k)

points = []
for point_idx in medoids:
    points.append({
        "lat": locations[point_idx][0]*1e-7,
        "lng": locations[point_idx][1]*1e-7,
    })

pois = json.dumps(points)
print(pois)
