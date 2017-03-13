SELECT airports.iata,
       airports.name,
       airport_rankings.rank,
       St_distance(airport_spatial.location, St_makepoint(22.28552, 114.15769)::geography) as distance
FROM   airports

INNER JOIN airport_spatial
      ON airports.id = airport_spatial.id 
      AND St_dwithin(
      	  airport_spatial.location, 
	  St_makepoint(22.28552, 114.15769)::geography, 50000)

LEFT JOIN airport_rankings
     ON airports.IATA = airport_rankings.IATA

ORDER BY airport_rankings.rank, St_distance(location, St_makepoint(22.28552, 114.15769) :: geography);
