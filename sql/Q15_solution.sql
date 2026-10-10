WITH events AS (
  SELECT start_at AS at,1 AS delta FROM meetings
  UNION ALL SELECT end_at,-1 FROM meetings
), grouped AS (SELECT at,SUM(delta) AS delta FROM events GROUP BY at),
swept AS (
  SELECT at,LEAD(at) OVER (ORDER BY at) AS until,
         SUM(delta) OVER (ORDER BY at ROWS UNBOUNDED PRECEDING) AS active
  FROM grouped
), segments AS (SELECT * FROM swept WHERE until>at),
peaks AS (SELECT *,MAX(active) OVER () AS peak FROM segments)
SELECT at AS start_at,until AS end_at,active FROM peaks WHERE active=peak ORDER BY at;
