SELECT p.id,COALESCE((
  SELECT c.price FROM changes c WHERE c.product_id=p.id AND c.day_no<=5
  ORDER BY c.day_no DESC LIMIT 1
),10) AS price FROM products p ORDER BY p.id;
