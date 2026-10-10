CREATE TABLE policies (
    id INTEGER PRIMARY KEY,
    prior_value INTEGER,
    current_value INTEGER,
    lat INTEGER,
    lon INTEGER
);

INSERT INTO policies (id, prior_value, current_value, lat, lon) VALUES
    (1, 10, 5, 1, 1),
    (2, 20, 20, 2, 2),
    (3, 10, 30, 2, 2),
    (4, 10, 40, 4, 4),
    (5, 99, 7, 5, 5);
