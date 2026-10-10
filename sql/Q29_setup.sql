CREATE TABLE students (
    id INTEGER PRIMARY KEY
);

INSERT INTO students (id) VALUES
    (1),
    (2),
    (3),
    (4),
    (5);

CREATE TABLE scores (
    exam_id INTEGER,
    student_id INTEGER,
    score INTEGER
);

INSERT INTO scores (exam_id, student_id, score) VALUES
    (1, 1, 10),
    (1, 2, 20),
    (1, 3, 30),
    (1, 4, 30),
    (2, 1, 40),
    (2, 2, 50),
    (2, 3, 60),
    (2, 4, 50);
