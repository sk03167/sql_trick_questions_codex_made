CREATE TABLE accounts (
    id INTEGER PRIMARY KEY,
    monthly_limit INTEGER
);

INSERT INTO accounts (id, monthly_limit) VALUES
    (1, 100),
    (2, 100),
    (3, 100);

CREATE TABLE credits (
    account_id INTEGER,
    month_index INTEGER,
    amount INTEGER
);

INSERT INTO credits (account_id, month_index, amount) VALUES
    (1, 24299, 60),
    (1, 24299, 60),
    (1, 24300, 110),
    (2, 24299, 120),
    (2, 24301, 130),
    (3, 24299, 100),
    (3, 24300, 150);
