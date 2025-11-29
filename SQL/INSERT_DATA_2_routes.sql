 -- ROUTES
INSERT INTO Bookings_route (origin_id, destination_id) VALUES
    (1, 2),   -- 1: London -> New York
    (2, 1),   -- 2: New York -> London
    (1, 3),   -- 3: London -> Boston
    (3, 1),   -- 4: Boston -> London
    (2, 4),   -- 5: New York -> Miami
    (4, 2),   -- 6: Miami -> New York
    (5, 6),   -- 7: Madrid -> Barcelona
    (6, 5),   -- 8: Barcelona -> Madrid
    (7, 8),   -- 9: Tokyo -> Sydney
    (8, 7);   -- 10: Sydney -> Tokyo


