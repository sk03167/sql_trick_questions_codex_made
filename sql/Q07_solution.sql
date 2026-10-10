WITH d AS (SELECT DISTINCT user_id,day_no FROM logins),
g AS (
  SELECT *,day_no-ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY day_no) AS island FROM d
), streaks AS (
  SELECT user_id,MIN(day_no) AS start_day,MAX(day_no) AS end_day,COUNT(*) AS days
  FROM g GROUP BY user_id,island
), ranked AS (
  SELECT *,MAX(days) OVER (PARTITION BY user_id) AS longest FROM streaks
)
SELECT user_id,start_day,end_day,days FROM ranked
WHERE days=longest ORDER BY user_id,start_day;
