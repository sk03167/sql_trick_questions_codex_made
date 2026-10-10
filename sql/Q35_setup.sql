CREATE TABLE calendar (
    day_no INTEGER PRIMARY KEY
);

INSERT INTO calendar (day_no) VALUES
    (1),
    (2),
    (3),
    (4);

CREATE TABLE activity (
    user_id INTEGER,
    day_no INTEGER
);

INSERT INTO activity (user_id, day_no) VALUES
    (1, 1),
    (1, 2),
    (1, 2),
    (2, 2),
    (3, 4);
