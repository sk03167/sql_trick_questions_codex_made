WITH g AS (
  SELECT *,start_day-ROW_NUMBER() OVER (ORDER BY start_day) AS island FROM tasks
)
SELECT MIN(start_day) AS project_start,MAX(end_day) AS project_end,
       MAX(end_day)-MIN(start_day) AS duration
FROM g GROUP BY island ORDER BY duration,project_start;
