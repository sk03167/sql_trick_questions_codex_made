CREATE TABLE facts (
    id INTEGER PRIMARY KEY,
    key_id INTEGER,
    at INTEGER
);

INSERT INTO facts (id, key_id, at) VALUES
    (1, 1, 4),
    (2, 1, 5),
    (3, 1, 10),
    (4, 2, 5);

CREATE TABLE versions (
    key_id INTEGER,
    valid_from INTEGER,
    valid_to INTEGER,
    label TEXT
);

INSERT INTO versions (key_id, valid_from, valid_to, label) VALUES
    (1, 1, 5, 'old'),
    (1, 5, 10, 'new'),
    (1, 10, NULL, 'latest');
