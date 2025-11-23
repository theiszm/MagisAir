-- CITIES --
INSERT INTO MagisAir_city (city, country, iata_code)
VALUES ('Manila', 'Philippines', 'MNL');

INSERT INTO MagisAir_city (city, country, iata_code)
VALUES ('Hong Kong', 'China', 'HKG');

-- ROUTES --
INSERT INTO MagisAir_route (origin_id, destination_id)
VALUES (1, 2);

-- FLIGHT SCHEDULES & COST --
INSERT INTO MagisAir_flight (flightcode, departuredate, departuretime, arrivaldate, arrivaltime, flightcost, route_id)
VALUES ('MA 800', '2026-03-10', '14:00:00', '2026-03-10', '17:30:00', 8500, 1);
