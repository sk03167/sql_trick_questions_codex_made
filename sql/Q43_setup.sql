CREATE TABLE players (
    id INTEGER PRIMARY KEY,
    group_id INTEGER
);

INSERT INTO players (id, group_id) VALUES
    (1, 1),
    (2, 1),
    (3, 1),
    (4, 2),
    (5, 2);

CREATE TABLE matches (
    id INTEGER PRIMARY KEY,
    first_player INTEGER,
    second_player INTEGER,
    first_score INTEGER,
    second_score INTEGER
);

INSERT INTO matches (id, first_player, second_player, first_score, second_score) VALUES
    (1, 1, 2, 3, 1),
    (2, 2, 3, 2, 3);
