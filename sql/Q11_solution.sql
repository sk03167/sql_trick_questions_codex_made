WITH g AS (
  SELECT *,id-ROW_NUMBER() OVER (ORDER BY id) AS island
  FROM visits WHERE people>=100
), c AS (SELECT *,COUNT(*) OVER (PARTITION BY island) AS run_length FROM g)
SELECT id,day_no,people FROM c WHERE run_length>=3 ORDER BY id;
