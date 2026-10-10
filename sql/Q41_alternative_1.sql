WITH n AS (
  SELECT val,LEAD(val,1) OVER (ORDER BY seq) AS v1,
             LEAD(val,2) OVER (ORDER BY seq) AS v2 FROM logs
)
SELECT DISTINCT val FROM n WHERE val=v1 AND val=v2 ORDER BY val;
