CREATE TABLE events (
    id INTEGER PRIMARY KEY,
    user_id INTEGER,
    kind TEXT,
    at INTEGER
);

INSERT INTO events (id, user_id, kind, at) VALUES
    (1, 1, 'view', 1),
    (2, 1, 'buy', 2),
    (3, 1, 'add', 3),
    (4, 1, 'buy', 4),
    (5, 2, 'buy', 1),
    (6, 2, 'add', 2),
    (7, 2, 'view', 3),
    (8, 3, 'view', 1),
    (9, 3, 'add', 1),
    (10, 3, 'buy', 2);
