CREATE TABLE routes (
    row_id INTEGER PRIMARY KEY,
    src TEXT,
    dst TEXT,
    dist INTEGER
);

INSERT INTO routes (row_id, src, dst, dist) VALUES
    (1, 'A', 'B', 10),
    (2, 'B', 'A', 10),
    (3, 'A', 'C', 5),
    (4, 'D', 'C', 7),
    (5, 'A', 'B', 10),
    (6, 'A', 'A', 0),
    (7, 'B', 'A', 12);
