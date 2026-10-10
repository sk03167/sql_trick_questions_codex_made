SELECT c.id FROM customers c
WHERE NOT EXISTS (
  SELECT 1 FROM required r WHERE NOT EXISTS (
    SELECT 1 FROM purchases p WHERE p.customer_id=c.id AND p.product=r.product
  )
) AND NOT EXISTS (
  SELECT 1 FROM purchases p WHERE p.customer_id=c.id AND NOT EXISTS (
    SELECT 1 FROM required r WHERE r.product=p.product
  )
) ORDER BY c.id;
