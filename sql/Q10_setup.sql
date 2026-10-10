CREATE TABLE daily (
    day_no INTEGER PRIMARY KEY,
    status TEXT
);

INSERT INTO daily (day_no, status) VALUES
    (1, 'up'),
    (2, 'up'),
    (3, NULL),
    (4, NULL),
    (6, NULL),
    (7, 'up');
