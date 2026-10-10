SELECT COALESCE(SUM(i.amount),0) AS approved_total
FROM invoices i WHERE EXISTS (
  SELECT 1 FROM tags t WHERE t.invoice_id=i.id AND t.tag='approved'
);
