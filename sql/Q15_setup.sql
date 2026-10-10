CREATE TABLE meetings (
    id INTEGER PRIMARY KEY,
    start_at INTEGER,
    end_at INTEGER
);

INSERT INTO meetings (id, start_at, end_at) VALUES
    (1, 1, 4),
    (2, 2, 5),
    (3, 4, 6),
    (4, 4, 7);
