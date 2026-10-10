WITH p AS (
  SELECT *,LAG(day_no) OVER (ORDER BY day_no) AS prev_day,
           LAG(status) OVER (ORDER BY day_no) AS prev_status FROM daily
), f AS (
  SELECT *,CASE WHEN day_no=prev_day+1 AND
    (status=prev_status OR (status IS NULL AND prev_status IS NULL))
    THEN 0 ELSE 1 END AS fresh FROM p
), g AS (
  SELECT *,SUM(fresh) OVER (ORDER BY day_no ROWS UNBOUNDED PRECEDING) AS island FROM f
)
SELECT status,MIN(day_no) AS start_day,MAX(day_no) AS end_day
FROM g GROUP BY island,status ORDER BY start_day;
