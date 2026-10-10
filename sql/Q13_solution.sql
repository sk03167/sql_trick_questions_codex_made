WITH p AS (
  SELECT *,MAX(end_at) OVER (ORDER BY start_at,end_at,id
    ROWS BETWEEN UNBOUNDED PRECEDING AND 1 PRECEDING) AS previous_max
  FROM intervals
), f AS (
  SELECT *,CASE WHEN previous_max IS NULL OR start_at>previous_max THEN 1 ELSE 0 END AS fresh FROM p
), g AS (
  SELECT *,SUM(fresh) OVER (ORDER BY start_at,end_at,id ROWS UNBOUNDED PRECEDING) AS island FROM f
)
SELECT MIN(start_at) AS start_at,MAX(end_at) AS end_at
FROM g GROUP BY island ORDER BY start_at;
