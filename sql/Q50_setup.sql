CREATE TABLE movements (
    id INTEGER PRIMARY KEY,
    product TEXT,
    kind TEXT,
    qty INTEGER,
    cost INTEGER
);

INSERT INTO movements (id, product, kind, qty, cost) VALUES
    (1, 'A', 'IN', 5, 10),
    (2, 'A', 'IN', 4, 20),
    (3, 'A', 'OUT', 7, NULL),
    (4, 'A', 'IN', 6, 30),
    (5, 'A', 'OUT', 5, NULL),
    (6, 'B', 'IN', 2, 7),
    (7, 'B', 'OUT', 2, NULL);
