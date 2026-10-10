CREATE TABLE customers (
    id INTEGER PRIMARY KEY
);

INSERT INTO customers (id) VALUES
    (1),
    (2),
    (3),
    (4),
    (5);

CREATE TABLE basket (
    customer_id INTEGER,
    product TEXT
);

INSERT INTO basket (customer_id, product) VALUES
    (1, 'A'),
    (1, 'A'),
    (1, 'B'),
    (2, 'B'),
    (2, 'A'),
    (3, 'A');
