SELECT c.id FROM customers c
LEFT JOIN purchases p ON p.customer_id=c.id
WHERE p.id IS NULL ORDER BY c.id;
