CREATE TABLE tx (
    id INTEGER PRIMARY KEY,
    at INTEGER,
    amount INTEGER
);

INSERT INTO tx (id, at, amount) VALUES
    (1, 1, 10),
    (2, 1, 20),
    (3, 2, 5);
