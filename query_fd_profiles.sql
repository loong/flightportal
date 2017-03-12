SELECT row_to_json(r)
FROM (SELECT array_agg(DISTINCT(flightdiary_comments.url)) AS urls
      FROM flightdiary_comments
     ) r
