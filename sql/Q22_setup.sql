CREATE TABLE customers (
    id INTEGER PRIMARY KEY
);

INSERT INTO customers (id) VALUES
    (1),
    (2);

CREATE TABLE orders (
    id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    amount INTEGER
);

INSERT INTO orders (id, customer_id, amount) VALUES
    (1, 1, 50),
    (2, 1, 50);

CREATE TABLE payments (
    id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    amount INTEGER
);

INSERT INTO payments (id, customer_id, amount) VALUES
    (1, 1, 30),
    (2, 1, 30),
    (3, 1, 40);
