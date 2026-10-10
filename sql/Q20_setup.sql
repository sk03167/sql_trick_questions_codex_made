CREATE TABLE customers (
    id INTEGER PRIMARY KEY
);

INSERT INTO customers (id) VALUES
    (1),
    (2),
    (3);

CREATE TABLE purchases (
    id INTEGER PRIMARY KEY,
    customer_id INTEGER
);

INSERT INTO purchases (id, customer_id) VALUES
    (1, 1),
    (2, NULL);
