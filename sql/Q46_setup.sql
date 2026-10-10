CREATE TABLE reports (
    manager_id INTEGER,
    employee_id INTEGER
);

INSERT INTO reports (manager_id, employee_id) VALUES
    (1, 2),
    (2, 3),
    (3, 1),
    (2, 4),
    (1, 2),
    (5, 6);
