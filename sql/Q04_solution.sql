WITH e AS (
  SELECT DISTINCT CASE WHEN src < dst THEN src ELSE dst END AS a,
                  CASE WHEN src < dst THEN dst ELSE src END AS b
  FROM edges WHERE src <> dst
)
SELECT x.a, x.b, y.b AS c
FROM e x JOIN e y ON x.b = y.a
JOIN e z ON z.a = x.a AND z.b = y.b
ORDER BY x.a, x.b, y.b;
