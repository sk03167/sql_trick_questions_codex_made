SELECT c.id,COUNT(o.id) AS paid_orders
FROM customers c LEFT JOIN orders o
  ON o.customer_id=c.id AND o.status='paid'
GROUP BY c.id ORDER BY c.id;
