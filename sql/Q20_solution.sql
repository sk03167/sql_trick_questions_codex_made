SELECT c.id FROM customers c
WHERE NOT EXISTS (SELECT 1 FROM purchases p WHERE p.customer_id=c.id)
ORDER BY c.id;
