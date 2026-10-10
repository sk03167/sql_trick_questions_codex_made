WITH d AS (SELECT DISTINCT value FROM observations),
p AS (SELECT value,LAG(value) OVER (ORDER BY value) AS prev FROM d),
g AS (SELECT value,SUM(CASE WHEN prev IS NULL OR value<>prev+1 THEN 1 ELSE 0 END)
      OVER (ORDER BY value ROWS UNBOUNDED PRECEDING) AS island FROM p)
SELECT MIN(value) AS start_value,MAX(value) AS end_value,COUNT(*) AS length
FROM g GROUP BY island ORDER BY start_value;
