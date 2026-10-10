SELECT n.id,CASE
  WHEN n.parent_id IS NULL THEN 'Root'
  WHEN EXISTS (SELECT 1 FROM nodes c WHERE c.parent_id=n.id) THEN 'Inner'
  ELSE 'Leaf' END AS node_type
FROM nodes n ORDER BY n.id;
