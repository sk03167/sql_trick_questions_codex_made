WITH candidates AS (
  SELECT t.id AS target_id,r.id AS reading_id,r.at,r.value,
    ROW_NUMBER() OVER (PARTITION BY t.id ORDER BY ABS(t.at-r.at),r.at,r.id) AS rn
  FROM targets t CROSS JOIN readings r
)
SELECT target_id,reading_id,value FROM candidates WHERE rn=1 ORDER BY target_id;
