SELECT a.row_id, a.src, a.dst, a.dist
FROM routes a
LEFT JOIN routes b
  ON b.row_id < a.row_id AND b.dist = a.dist
 AND ((b.src = a.src AND b.dst = a.dst)
   OR (b.src = a.dst AND b.dst = a.src))
WHERE b.row_id IS NULL
ORDER BY a.row_id;
