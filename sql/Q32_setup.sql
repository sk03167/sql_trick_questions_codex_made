CREATE TABLE events (
    id INTEGER PRIMARY KEY,
    user_id INTEGER,
    at INTEGER,
    val INTEGER
);

INSERT INTO events (id, user_id, at, val) VALUES
    (1, 1, 1, 10),
    (2, 1, 2, 5),
    (3, 2, 1, 7),
    (4, 2, 2, NULL);
