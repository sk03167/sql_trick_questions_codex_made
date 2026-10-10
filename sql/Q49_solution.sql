WITH s AS (
  SELECT id,qty,SUM(qty) OVER (ORDER BY id ROWS UNBOUNDED PRECEDING) AS hi FROM supplies
), d AS (
  SELECT id,qty,SUM(qty) OVER (ORDER BY id ROWS UNBOUNDED PRECEDING) AS hi FROM demands
)
SELECT d.id AS demand_id,s.id AS supply_id,
  CASE WHEN s.hi<d.hi THEN s.hi ELSE d.hi END
    -CASE WHEN s.hi-s.qty>d.hi-d.qty THEN s.hi-s.qty ELSE d.hi-d.qty END AS allocated
FROM s JOIN d ON s.hi>d.hi-d.qty AND d.hi>s.hi-s.qty
ORDER BY d.id,s.id;
