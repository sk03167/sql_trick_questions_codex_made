WITH d AS (SELECT DISTINCT value FROM observations),
g AS (SELECT value, value-ROW_NUMBER() OVER (ORDER BY value) AS island FROM d)
SELECT MIN(value) AS start_value, MAX(value) AS end_value, COUNT(*) AS length
FROM g GROUP BY island ORDER BY start_value;
