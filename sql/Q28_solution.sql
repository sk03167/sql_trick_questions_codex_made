SELECT a.id AS a,b.id AS b FROM customers a JOIN customers b ON a.id<b.id
WHERE NOT EXISTS (
  SELECT 1 FROM basket x WHERE x.customer_id=a.id AND NOT EXISTS (
    SELECT 1 FROM basket y WHERE y.customer_id=b.id AND y.product=x.product
  )
) AND NOT EXISTS (
  SELECT 1 FROM basket y WHERE y.customer_id=b.id AND NOT EXISTS (
    SELECT 1 FROM basket x WHERE x.customer_id=a.id AND x.product=y.product
  )
) ORDER BY a.id,b.id;
