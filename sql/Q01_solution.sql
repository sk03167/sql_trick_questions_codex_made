WITH canonical AS (
  SELECT *, CASE WHEN src <= dst THEN src ELSE dst END AS lo,
            CASE WHEN src <= dst THEN dst ELSE src END AS hi
  FROM routes
), keep AS (
  SELECT MIN(row_id) AS row_id FROM canonical GROUP BY lo, hi, dist
)
SELECT r.row_id, r.src, r.dst, r.dist
FROM routes r JOIN keep k ON r.row_id = k.row_id
ORDER BY r.row_id;
