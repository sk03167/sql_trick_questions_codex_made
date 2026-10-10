CREATE TABLE old_snapshot (
    id INTEGER PRIMARY KEY,
    val TEXT
);

INSERT INTO old_snapshot (id, val) VALUES
    (1, 'a'),
    (2, NULL),
    (3, 'c'),
    (5, NULL);

CREATE TABLE new_snapshot (
    id INTEGER PRIMARY KEY,
    val TEXT
);

INSERT INTO new_snapshot (id, val) VALUES
    (1, 'a'),
    (2, 'b'),
    (4, 'd'),
    (5, NULL);
