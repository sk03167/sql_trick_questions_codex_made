WITH RECURSIVE calendar(day_no) AS (
  SELECT 1 UNION ALL SELECT day_no+1 FROM calendar WHERE day_no<5
), totals AS (SELECT day_no,SUM(amount) AS amount FROM sales GROUP BY day_no),
daily AS (
  SELECT c.day_no,COALESCE(t.amount,0) AS amount FROM calendar c LEFT JOIN totals t ON t.day_no=c.day_no
), rolled AS (
  SELECT day_no,SUM(amount) OVER (ORDER BY day_no ROWS BETWEEN 2 PRECEDING AND CURRENT ROW) AS window_total FROM daily
)
SELECT day_no,window_total,ROUND(window_total/3.0,2) AS average
FROM rolled WHERE day_no>=3 ORDER BY day_no;
