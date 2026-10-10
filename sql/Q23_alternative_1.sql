WITH eligible AS (
  SELECT DISTINCT invoice_id FROM tags WHERE tag='approved'
)
SELECT COALESCE(SUM(i.amount),0) AS approved_total
FROM invoices i JOIN eligible e ON e.invoice_id=i.id;
