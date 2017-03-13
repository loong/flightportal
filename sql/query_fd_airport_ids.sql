SELECT row_to_json(r)
FROM (SELECT array_agg(flightdiary_airports.id) AS ids
      FROM flightdiary_airports
     ) r
