WITH totals AS (
  SELECT *,SUM(weight) OVER (ORDER BY turn ROWS UNBOUNDED PRECEDING) AS cumulative FROM queue
)
SELECT turn,name FROM totals WHERE cumulative<=1000 ORDER BY turn DESC LIMIT 1;
