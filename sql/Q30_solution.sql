WITH flagged AS (
  SELECT *,COUNT(*) OVER (PARTITION BY prior_value) AS prior_count,
           COUNT(*) OVER (PARTITION BY lat,lon) AS location_count FROM policies
)
SELECT COALESCE(SUM(current_value),0) AS total FROM flagged
WHERE prior_count>1 AND location_count=1;
