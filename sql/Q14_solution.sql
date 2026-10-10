WITH p AS (
  SELECT *,MAX(end_at) OVER (ORDER BY start_at,end_at,id
    ROWS BETWEEN UNBOUNDED PRECEDING AND 1 PRECEDING) AS mx FROM bookings
), f AS (
  SELECT *,CASE WHEN mx IS NULL OR start_at>mx THEN 1 ELSE 0 END AS fresh FROM p
), g AS (
  SELECT *,SUM(fresh) OVER (ORDER BY start_at,end_at,id ROWS UNBOUNDED PRECEDING) AS grp FROM f
), packed AS (
  SELECT MIN(start_at) AS s,MAX(end_at) AS e FROM g GROUP BY grp
), padded AS (
  SELECT s,e FROM packed UNION ALL SELECT 0,0 UNION ALL SELECT 20,20
), gaps AS (
  SELECT e AS free_start,LEAD(s) OVER (ORDER BY s,e) AS free_end FROM padded
)
SELECT free_start,free_end FROM gaps WHERE free_end>free_start ORDER BY free_start;
