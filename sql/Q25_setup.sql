CREATE TABLE old_bag (
    key_name TEXT
);

INSERT INTO old_bag (key_name) VALUES
    ('a'),
    ('a'),
    ('b'),
    (NULL);

CREATE TABLE new_bag (
    key_name TEXT
);

INSERT INTO new_bag (key_name) VALUES
    ('a'),
    ('b'),
    ('b'),
    ('c'),
    (NULL),
    (NULL);
