CREATE TABLE invoices (
    id INTEGER PRIMARY KEY,
    amount INTEGER
);

INSERT INTO invoices (id, amount) VALUES
    (1, 50),
    (2, 50),
    (3, 100);

CREATE TABLE tags (
    invoice_id INTEGER,
    tag TEXT
);

INSERT INTO tags (invoice_id, tag) VALUES
    (1, 'approved'),
    (1, 'approved'),
    (2, 'approved'),
    (3, 'draft');
