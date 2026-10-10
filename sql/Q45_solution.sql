WITH monthly AS (
  SELECT c.account_id,c.month_index,SUM(c.amount) AS total
  FROM credits c GROUP BY c.account_id,c.month_index
), over_limit AS (
  SELECT m.* FROM monthly m JOIN accounts a ON a.id=m.account_id WHERE m.total>a.monthly_limit
), adjacent AS (
  SELECT *,LAG(month_index) OVER (PARTITION BY account_id ORDER BY month_index) AS prev FROM over_limit
)
SELECT DISTINCT account_id FROM adjacent WHERE month_index=prev+1 ORDER BY account_id;
