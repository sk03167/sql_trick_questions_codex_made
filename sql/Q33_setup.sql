CREATE TABLE readings (
    id INTEGER PRIMARY KEY,
    user_id INTEGER,
    at INTEGER,
    val INTEGER
);

INSERT INTO readings (id, user_id, at, val) VALUES
    (1, 1, 1, NULL),
    (2, 1, 2, 10),
    (3, 1, 3, NULL),
    (4, 1, 4, 3),
    (5, 1, 5, NULL),
    (6, 2, 1, -2),
    (7, 2, 2, NULL);
