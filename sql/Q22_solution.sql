WITH o AS (SELECT customer_id,SUM(amount) AS total FROM orders GROUP BY customer_id),
p AS (SELECT customer_id,SUM(amount) AS total FROM payments GROUP BY customer_id)
SELECT c.id,COALESCE(o.total,0) AS ordered,COALESCE(p.total,0) AS paid
FROM customers c LEFT JOIN o ON o.customer_id=c.id
LEFT JOIN p ON p.customer_id=c.id ORDER BY c.id;
