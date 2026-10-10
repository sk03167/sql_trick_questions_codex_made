CREATE TABLE supplies (
    id INTEGER PRIMARY KEY,
    qty INTEGER
);

INSERT INTO supplies (id, qty) VALUES
    (1, 5),
    (2, 4),
    (3, 6);

CREATE TABLE demands (
    id INTEGER PRIMARY KEY,
    qty INTEGER
);

INSERT INTO demands (id, qty) VALUES
    (1, 7),
    (2, 5);
