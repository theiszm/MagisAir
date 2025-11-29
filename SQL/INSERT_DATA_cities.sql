-- CITIES --
INSERT INTO Bookings_city (city, country, iata_code)
VALUES 
	('Manila', 'Philippines', 'MNL'),
	('Hong Kong', 'China', 'HKG'),
    ('Boston, Massachusetts','United States','BOS'),
    ('New York, New York','United States','JFK'),
    ('Miami, Florida','United States','MIA'),
    ('London','United Kingdom','LHR'),
    ('Barcelona','Spain','BCN'),
    ('Madrid','Spain','MAD');

-- ROUTES --
INSERT INTO Bookings_route (origin_id, destination_id)
VALUES 
    (1, 2),   -- Manila -> Hong Kong
    (2, 1),   -- Hong Kong -> Manila
    (3, 6),
    (4, 6),
    (4, 8),
    (5, 6),
    (5, 8),
    (6, 3),
    (6, 4),
    (6, 5);


-- FLIGHT SCHEDULES & COST --
INSERT INTO Bookings_flight (flight_code, departure, arrival, route_id, base_fare)
VALUES
    -- Flight MA 800 (Manila -> Hong Kong)
    ('MA 800', '2026-03-10 14:00:00', '2026-03-10 17:30:00', 1, 8500),
    -- Flight MA 801 (Hong Kong -> Manila)
    ('MA 801', '2026-03-15 12:00:00', '2026-03-15 15:30:00', 2, 8300),
    -- Flight MA 900 (Boston -> London)
    ('MA 100', '2026-04-01 19:00:00', '2026-04-02 07:00:00', 3, 4500),
    -- Flight MA 901 (New York -> London)
    ('MA 200', '2026-04-03 20:00:00', '2026-04-04 08:00:00', 4, 4700),
    -- Flight MA 902 (New York -> Barcelona)
    ('MA 210', '2026-04-05 18:00:00', '2026-04-06 06:30:00', 5, 5200),
    -- Flight MA 903 (Miami -> London)
    ('MA 300', '2026-04-07 21:00:00', '2026-04-08 09:00:00', 6, 4800),
    -- Flight MA 904 (Miami -> Madrid)
    ('MA 310', '2026-04-09 22:00:00', '2026-04-10 10:30:00', 7, 5300),
    -- Flight MA 905 (London -> Boston)
    ('MA 150', '2026-04-11 10:00:00', '2026-04-11 20:00:00', 8, 4400),
    -- Flight MA 906 (London -> New York)
    ('MA 250', '2026-04-12 11:00:00', '2026-04-12 21:00:00', 9, 4600),
    -- Flight MA 907 (London -> Miami)
    ('MA 350', '2026-04-13 12:00:00', '2026-04-13 22:30:00', 10, 4900);
    