WITH bounds AS (
  SELECT val,freq,SUM(freq) OVER (ORDER BY val ROWS UNBOUNDED PRECEDING) AS hi,
                  SUM(freq) OVER () AS n FROM frequencies
), positions AS (
  SELECT (SUM(freq)+1)/2 AS p FROM frequencies
  UNION ALL SELECT (SUM(freq)+2)/2 FROM frequencies
)
SELECT AVG(b.val*1.0) AS median
FROM positions p JOIN bounds b ON p.p>b.hi-b.freq AND p.p<=b.hi;
