CREATE TABLE people (
    id INTEGER PRIMARY KEY
);

INSERT INTO people (id) VALUES
    (1),
    (2),
    (3),
    (4);

CREATE TABLE edges (
    a INTEGER,
    b INTEGER
);

INSERT INTO edges (a, b) VALUES
    (1, 2),
    (2, 1),
    (1, 2),
    (2, 3),
    (3, 3);
