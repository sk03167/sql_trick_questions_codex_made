CREATE TABLE products (
    id INTEGER PRIMARY KEY
);

INSERT INTO products (id) VALUES
    (1),
    (2),
    (3),
    (4);

CREATE TABLE changes (
    product_id INTEGER,
    day_no INTEGER,
    price INTEGER
);

INSERT INTO changes (product_id, day_no, price) VALUES
    (1, 2, 20),
    (1, 5, 30),
    (1, 8, 99),
    (2, 7, 40),
    (3, 3, 15);
