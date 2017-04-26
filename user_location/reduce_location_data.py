import json

with open('locations.json') as json_data:
    data = json.load(json_data)
    data_size = len(data["locations"])

print("Number of locations found: %d" % data_size) 

points = {'locations':[]}

for loc in data["locations"]:
        if "latitudeE7" in loc:
            lat, lon = loc["latitudeE7"], loc["longitudeE7"]
            points['locations'].append({'latitudeE7': lat, 'longitudeE7': lon})

print("Write results to minified_locations.json")
with open('../datastore/sources/minified_locations.json', 'w') as outfile:
    json.dump(points, outfile)
