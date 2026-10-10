WITH p AS (
  SELECT *,LAG(minute_no) OVER (PARTITION BY user_id ORDER BY minute_no,event_id) AS prev FROM events
), f AS (
  SELECT *,CASE WHEN prev IS NULL OR minute_no-prev>30 THEN 1 ELSE 0 END AS fresh FROM p
), g AS (
  SELECT *,SUM(fresh) OVER (PARTITION BY user_id ORDER BY minute_no,event_id ROWS UNBOUNDED PRECEDING) AS session_no FROM f
)
SELECT user_id,session_no,MIN(minute_no) AS start_minute,MAX(minute_no) AS end_minute,COUNT(*) AS events
FROM g GROUP BY user_id,session_no ORDER BY user_id,session_no;
