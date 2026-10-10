SELECT DISTINCT a.x, a.y
FROM pairs a JOIN pairs b
  ON a.x = b.y AND a.y = b.x AND a.id <> b.id
WHERE a.x <= a.y
ORDER BY a.x, a.y;
