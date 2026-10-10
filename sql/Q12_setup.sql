CREATE TABLE tasks (
    id INTEGER PRIMARY KEY,
    start_day INTEGER,
    end_day INTEGER
);

INSERT INTO tasks (id, start_day, end_day) VALUES
    (1, 1, 2),
    (2, 2, 3),
    (3, 5, 6),
    (4, 8, 9),
    (5, 9, 10),
    (6, 10, 11);
