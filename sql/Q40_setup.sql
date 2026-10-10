CREATE TABLE events (
    seq INTEGER PRIMARY KEY,
    is_reset INTEGER,
    amount INTEGER
);

INSERT INTO events (seq, is_reset, amount) VALUES
    (1, 0, 5),
    (2, 0, 3),
    (3, 1, 0),
    (4, 0, 4),
    (5, 0, -1),
    (6, 1, 0),
    (7, 0, 2);
