CREATE TABLE customers (
    id INTEGER PRIMARY KEY
);

INSERT INTO customers (id) VALUES
    (1),
    (2),
    (3),
    (4);

CREATE TABLE required (
    product TEXT PRIMARY KEY
);

INSERT INTO required (product) VALUES
    ('A'),
    ('B');

CREATE TABLE purchases (
    customer_id INTEGER,
    product TEXT
);

INSERT INTO purchases (customer_id, product) VALUES
    (1, 'A'),
    (1, 'B'),
    (1, 'X'),
    (2, 'A'),
    (3, 'A'),
    (3, 'A'),
    (3, 'B');
