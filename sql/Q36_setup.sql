CREATE TABLE events (
    id INTEGER PRIMARY KEY,
    at INTEGER,
    user_id INTEGER
);

INSERT INTO events (id, at, user_id) VALUES
    (1, 1, 8),
    (2, 1, 8),
    (3, 2, 9),
    (4, 3, NULL),
    (5, 4, 8),
    (6, 5, 10);
