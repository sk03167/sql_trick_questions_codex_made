WITH g AS (
  SELECT *,COUNT(val) OVER (PARTITION BY user_id ORDER BY at,id ROWS UNBOUNDED PRECEDING) AS grp FROM readings
)
SELECT id,MAX(val) OVER (PARTITION BY user_id,grp) AS filled_value FROM g ORDER BY id;
