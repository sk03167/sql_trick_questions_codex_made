WITH RECURSIVE e(a,b) AS (
  SELECT a,b FROM edges UNION SELECT b,a FROM edges
), reach(root,node) AS (
  SELECT id,id FROM nodes
  UNION
  SELECT r.root,e.b FROM reach r JOIN e ON e.a=r.node
)
SELECT node, MIN(root) AS component
FROM reach GROUP BY node ORDER BY node;
