CREATE TABLE intervals (
    id INTEGER PRIMARY KEY,
    start_at INTEGER,
    end_at INTEGER
);

INSERT INTO intervals (id, start_at, end_at) VALUES
    (1, 1, 10),
    (2, 2, 3),
    (3, 4, 8),
    (4, 10, 12),
    (5, 15, 17);
