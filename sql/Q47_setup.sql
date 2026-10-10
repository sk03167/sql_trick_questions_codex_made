CREATE TABLE nodes (
    id INTEGER PRIMARY KEY,
    parent_id INTEGER
);

INSERT INTO nodes (id, parent_id) VALUES
    (1, NULL),
    (2, 1),
    (3, 1),
    (4, 2),
    (9, NULL);
