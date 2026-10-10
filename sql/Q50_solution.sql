WITH incoming AS (
  SELECT *,SUM(qty) OVER (PARTITION BY product ORDER BY id ROWS UNBOUNDED PRECEDING) AS hi
  FROM movements WHERE kind='IN'
), sold AS (
  SELECT product,SUM(CASE WHEN kind='OUT' THEN qty ELSE 0 END) AS qty
  FROM movements GROUP BY product
), leftovers AS (
  SELECT i.product,i.cost,CASE
    WHEN i.hi<=s.qty THEN 0
    WHEN i.hi-i.qty>=s.qty THEN i.qty
    ELSE i.hi-s.qty END AS remaining
  FROM incoming i JOIN sold s ON s.product=i.product
)
SELECT product,SUM(remaining) AS remaining_qty,SUM(remaining*cost) AS inventory_value
FROM leftovers GROUP BY product ORDER BY product;
