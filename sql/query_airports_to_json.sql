SELECT row_to_json(t) 
FROM ( select name, iata, country from airports ) t 
