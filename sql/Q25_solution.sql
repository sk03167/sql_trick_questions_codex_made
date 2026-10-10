WITH signed AS (
  SELECT key_name,-1 AS delta FROM old_bag
  UNION ALL SELECT key_name,1 FROM new_bag
)
SELECT key_name,SUM(delta) AS delta FROM signed
GROUP BY key_name HAVING SUM(delta)<>0
ORDER BY CASE WHEN key_name IS NULL THEN 0 ELSE 1 END,key_name;
