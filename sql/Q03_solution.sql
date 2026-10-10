WITH directed AS (
  SELECT a AS person, b AS neighbor FROM edges WHERE a <> b
  UNION
  SELECT b, a FROM edges WHERE a <> b
)
SELECT p.id, COUNT(d.neighbor) AS neighbors
FROM people p LEFT JOIN directed d ON d.person = p.id
GROUP BY p.id ORDER BY p.id;
