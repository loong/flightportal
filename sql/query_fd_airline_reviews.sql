SELECT content, helpful_percentage, rating, helpful_percentage
FROM flightdiary_airline_comments
WHERE airline_id = (SELECT id FROM flightdiary_airlines WHERE iata = 'CX' LIMIT 1)
ORDER BY helpful_percentage DESC
LIMIT 10;
