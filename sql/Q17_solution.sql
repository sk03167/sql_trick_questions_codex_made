WITH eligible AS (
  SELECT *,ROW_NUMBER() OVER (PARTITION BY product_id ORDER BY day_no DESC) AS rn
  FROM changes WHERE day_no<=5
)
SELECT p.id,COALESCE(e.price,10) AS price
FROM products p LEFT JOIN eligible e ON e.product_id=p.id AND e.rn=1
ORDER BY p.id;
