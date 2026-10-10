WITH points AS (
  SELECT 0 AS id UNION SELECT id FROM ids UNION SELECT 13
), n AS (SELECT id,LEAD(id) OVER (ORDER BY id) AS next_id FROM points)
SELECT id+1 AS gap_start,next_id-1 AS gap_end
FROM n WHERE next_id > id+1 ORDER BY gap_start;
