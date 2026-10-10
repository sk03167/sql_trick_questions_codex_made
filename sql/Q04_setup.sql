CREATE TABLE edges (
    src INTEGER,
    dst INTEGER
);

INSERT INTO edges (src, dst) VALUES
    (1, 2),
    (2, 1),
    (2, 3),
    (1, 3),
    (1, 4),
    (3, 4),
    (4, 4);
