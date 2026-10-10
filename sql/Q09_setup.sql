CREATE TABLE events (
    event_id INTEGER PRIMARY KEY,
    user_id INTEGER,
    minute_no INTEGER
);

INSERT INTO events (event_id, user_id, minute_no) VALUES
    (1, 1, 0),
    (2, 1, 30),
    (3, 1, 61),
    (4, 1, 61),
    (5, 2, 5),
    (6, 2, 40);
