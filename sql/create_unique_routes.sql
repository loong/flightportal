INSERT INTO routes_unique(src, dest)
SELECT src_airport as src, dest_airport as dest
FROM routes
ON CONFLICT (src, dest) DO NOTHING;
