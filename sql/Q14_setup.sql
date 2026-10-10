CREATE TABLE bookings (
    id INTEGER PRIMARY KEY,
    start_at INTEGER,
    end_at INTEGER
);

INSERT INTO bookings (id, start_at, end_at) VALUES
    (1, 1, 5),
    (2, 3, 7),
    (3, 10, 12),
    (4, 12, 16);
