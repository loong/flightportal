import json
import numpy as np
from sklearn import cluster

with open('locations.json') as json_data:
    data = json.load(json_data)
    data_size = len(data["locations"])
    
    print("# of locations %d" % data_size)

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

    k = 20
    kmeans = cluster.KMeans(n_clusters=k, n_jobs=-2) #use all but one cpu
    data = np.array(locations, np.int32)
    print(data[0:5])
    print()
    kmeans.fit(data)

    centroids = kmeans.cluster_centers_

    print(centroids)
    
    points = []
    for centroid in centroids:
        points.append({
            "lat": centroid[0]*1e-7,
            "lng": centroid[1]*1e-7
        })

    pois = json.dumps(points)

    print(pois)
