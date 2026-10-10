CREATE TABLE customers (
    id INTEGER PRIMARY KEY
);

INSERT INTO customers (id) VALUES
    (1),
    (2),
    (3);

CREATE TABLE orders (
    id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    status TEXT
);

INSERT INTO orders (id, customer_id, status) VALUES
    (11, 1, 'paid'),
    (12, 1, 'cancelled'),
    (13, 2, 'cancelled');
