CREATE TABLE nodes (
    id INTEGER PRIMARY KEY
);

INSERT INTO nodes (id) VALUES
    (1),
    (2),
    (3),
    (4),
    (5),
    (6);

CREATE TABLE edges (
    a INTEGER,
    b INTEGER
);

INSERT INTO edges (a, b) VALUES
    (1, 2),
    (2, 3),
    (3, 1),
    (4, 5),
    (1, 2);
