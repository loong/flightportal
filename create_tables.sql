CREATE TABLE IF NOT EXISTS airports(
       id int PRIMARY KEY UNIQUE,
       name varchar,
       city varchar,
       country varchar,
       IATA char(3) NULL,
       ICAO char(4) NULL,
       latitude double precision,
       longitude double precision,
       altitude_ft int,
       timezone_utc float,
       DST char(1),
       timezone_tz varchar,
       type varchar,
       source varchar
);

CREATE TABLE IF NOT EXISTS airport_rankings(
       IATA char(3) NOT NULL UNIQUE,
       rank int,
       passengers int
);

CREATE TABLE IF NOT EXISTS airport_spatial(
       id int PRIMARY KEY UNIQUE,
       location geography(Point,4326)
);


CREATE TABLE IF NOT EXISTS flightdiary_airports(
       name varchar,
       url varchar,
       country varchar,
       IATA char(3) NULL,
       lon double precision,
       value varchar,	      
       label varchar,
       ICAO char(4) NULL,
       lat double precision,
       id int PRIMARY KEY UNIQUE
);

CREATE TABLE IF NOT EXISTS flightdiary_comments(
       _type varchar,
       airport_id int,
       content text,
       extra varchar,
       facebook varchar,
       helpful_percentage int,
       id int PRIMARY KEY UNIQUE,
       is_voted boolean,
       name varchar,
       page int,
       rating smallint,
       reported varchar,
       time varchar,
       timestamp varchar,
       total_no int,
       total_yes int,
       url varchar
);
