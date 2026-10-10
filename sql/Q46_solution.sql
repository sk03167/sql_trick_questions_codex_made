WITH RECURSIVE reachable(id) AS (
  SELECT 1
  UNION
  SELECT r.employee_id FROM reports r JOIN reachable x ON r.manager_id=x.id
)
SELECT id FROM reachable WHERE id<>1 ORDER BY id;
