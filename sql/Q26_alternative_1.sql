SELECT c.id FROM customers c
LEFT JOIN purchases p ON p.customer_id=c.id
LEFT JOIN required r ON r.product=p.product
GROUP BY c.id
HAVING COUNT(DISTINCT r.product)=(SELECT COUNT(*) FROM required)
ORDER BY c.id;
