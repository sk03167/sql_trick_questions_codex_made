CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    signup_day INTEGER
);

INSERT INTO users (id, signup_day) VALUES
    (1, 1),
    (2, 1),
    (3, 1),
    (4, 2),
    (5, 2);

CREATE TABLE activity (
    user_id INTEGER,
    day_no INTEGER
);

INSERT INTO activity (user_id, day_no) VALUES
    (1, 2),
    (1, 2),
    (2, 3),
    (4, 3),
    (5, 3);
