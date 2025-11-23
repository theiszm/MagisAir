-- CITIES --
INSERT INTO MagisAir_city (city, country, iata_code)
VALUES 
	('Manila', 'Philippines', 'MNL'),
	('Hong Kong', 'China', 'HKG');

-- ROUTES --
INSERT INTO MagisAir_route (origin_id, destination_id)
VALUES 
    (1, 2),   -- Manila -> Hong Kong
    (2, 1);   -- Hong Kong -> Manila

-- FLIGHT SCHEDULES & COST --
INSERT INTO MagisAir_flight (flight_code, departure_date, departure_time, arrival_date, arrival_time, route_id, base_fare)
VALUES
    -- Flight MA 800 (Manila -> Hong Kong)
    ('MA 800', '2026-03-10', '14:00:00', '2026-03-10', '17:30:00', 1, 8500),
    -- Flight MA 801 (Hong Kong -> Manila)
    ('MA 801', '2026-03-15', '12:00:00', '2026-03-15', '15:30:00', 2, 8300);