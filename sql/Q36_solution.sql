WITH marked AS (
  SELECT *,ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY at,id) AS occurrence FROM events
)
SELECT id,SUM(CASE WHEN user_id IS NOT NULL AND occurrence=1 THEN 1 ELSE 0 END)
  OVER (ORDER BY at,id ROWS UNBOUNDED PRECEDING) AS distinct_users
FROM marked ORDER BY at,id;
