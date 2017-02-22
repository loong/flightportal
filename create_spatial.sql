INSERT INTO airport_spatial(id, location)
SELECT id, ST_MakePoint(latitude, longitude) as location FROM airports;

CREATE index airport_spatial_location_idx on airport_spatial using gist(location);

