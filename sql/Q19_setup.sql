CREATE TABLE targets (
    id INTEGER PRIMARY KEY,
    at INTEGER
);

INSERT INTO targets (id, at) VALUES
    (1, 5),
    (2, 10),
    (3, 0);

CREATE TABLE readings (
    id INTEGER PRIMARY KEY,
    at INTEGER,
    value INTEGER
);

INSERT INTO readings (id, at, value) VALUES
    (1, 3, 30),
    (2, 7, 70),
    (3, 7, 71),
    (4, 12, 120);
