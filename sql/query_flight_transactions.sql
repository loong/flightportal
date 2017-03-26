select array_agg(concat(from_iata, '->', to_iata)) from flightdiary_flights username group by username;
