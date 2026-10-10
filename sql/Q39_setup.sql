CREATE TABLE queue (
    turn INTEGER PRIMARY KEY,
    name TEXT,
    weight INTEGER
);

INSERT INTO queue (turn, name, weight) VALUES
    (1, 'Ana', 400),
    (2, 'Ben', 350),
    (3, 'Cy', 250),
    (4, 'Di', 1),
    (5, 'Eli', 10);
