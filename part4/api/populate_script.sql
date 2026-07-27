-- DELETE FROM users;
-- DELETE FROM places;
-- DELETE FROM amenities;
-- DELETE FROM place_amenity;

-- DROP TABLE amenities;

-- ALTER TABLE amenities DROP COLUMN place_id;

INSERT INTO users (id, first_name, last_name, email, password, is_admin) VALUES
('9b17d3fd-4e2b-4c9a-b0db-9e3b50e3f001', 'John', 'Doe', 'john@example.com', '$2y$10$87o.xFePu5q847uwJjfPL.GBE5jvYM.pVKl6ZIi/Pl5MOXZ8YjGGm', 1),
('9b17d3fd-4e2b-4c9a-b0db-9e3b50e3f002', 'Jane', 'Smith', 'jane@example.com', '$2y$10$qM5AWuTp3slrwIurNUmVe.AXbfjWgRZGMRfE3PhnBAzHyh.sl98CC', 0),
('9b17d3fd-4e2b-4c9a-b0db-9e3b50e3f003', 'Alice', 'Brown', 'alice@example.com', '$2y$10$ETNOKqNTfNym3y7lyn7Sw.fBjjyeViqWypxFOE2/MTffwhEoIfpAe', 0),
('36c9050e-ddd3-4c3b-9731-9f487208bbc1', 'Admin', 'HBnB', 'admin@hbnb.io', '$2y$10$i207gAEK9fOUmU1fpp/eGOIAMToVocjzSM.Kxh2bla9JMDlog.e9S', 1);

INSERT INTO places (id, title, description, price, latitude, longitude, owner_id) VALUES
(
    'f31a4e7a-1111-4444-8888-aaaaaaaaaaaa',
    'Beach House',
    'Beautiful ocean view',
    250.00,
    -37.8136,
    144.9631,
    '9b17d3fd-4e2b-4c9a-b0db-9e3b50e3f001'
);
INSERT INTO places (id, title, description, price, latitude, longitude, owner_id) VALUES
(
    'f31a4e7a-2222-4444-8888-bbbbbbbbbbbb',
    'City Apartment',
    'Close to downtown',
    150.00,
    -37.8140,
    144.9650,
    '9b17d3fd-4e2b-4c9a-b0db-9e3b50e3f002'
);
INSERT INTO places (id, title, description, price, latitude, longitude, owner_id) VALUES
(
    'b9b81b15-6540-4eea-961a-5c39c5baba2e',
    'Town house',
    'Close to Mine field',
    120.00,
    -30.8140,
    122.9650,
    '36c9050e-ddd3-4c3b-9731-9f487208bbc1'
);

INSERT INTO amenities (id, name) VALUES
("f31a4e7a-1111-3223-8888-aaaaaaaaaaaa", "WIFI"),
("f31a4e7a-1111-4444-8888-avc982vbasdf", "Swimming pool"),
("f31a4e7a-1111-4444-3488-avc982vbasdf", "Air conditioner");

INSERT INTO place_amenity (place_id, amenity_id) VALUES
("f31a4e7a-1111-4444-8888-aaaaaaaaaaaa", "f31a4e7a-1111-3223-8888-aaaaaaaaaaaa"),
("f31a4e7a-2222-4444-8888-bbbbbbbbbbbb", "f31a4e7a-1111-3223-8888-aaaaaaaaaaaa"),
("f31a4e7a-2222-4444-8888-bbbbbbbbbbbb", "f31a4e7a-1111-4444-8888-avc982vbasdf");

SELECT CONCAT(CHAR(10), 'user data ----------------------------', CHAR(10));
SELECT * FROM users;
SELECT CONCAT(CHAR(10), 'place data ----------------------------', CHAR(10));
SELECT * FROM places;
SELECT CONCAT(CHAR(10), 'amenities ----------------------------', CHAR(10));
SELECT * FROM amenities;
SELECT CONCAT(CHAR(10), 'place_amenities ----------------------------', CHAR(10));
SELECT * FROM place_amenity;

PRAGMA table_info(amenities)
