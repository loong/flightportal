SELECT row_to_json(r)
FROM (SELECT array_agg(airports.IATA) AS a
      FROM airports
      WHERE airports.IATA IS NOT NULL
     ) r
