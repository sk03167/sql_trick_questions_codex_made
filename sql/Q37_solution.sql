WITH ordered AS (
  SELECT *,ROW_NUMBER() OVER (PARTITION BY company ORDER BY salary,id) AS rn,
           COUNT(*) OVER (PARTITION BY company) AS n FROM employees
)
SELECT company,AVG(salary*1.0) AS median FROM ordered
WHERE rn BETWEEN (n+1)/2 AND (n+2)/2
GROUP BY company ORDER BY company;
