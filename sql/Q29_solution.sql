WITH limits AS (
  SELECT exam_id,MIN(score) AS lo,MAX(score) AS hi FROM scores GROUP BY exam_id
)
SELECT s.id FROM students s
WHERE EXISTS (SELECT 1 FROM scores x WHERE x.student_id=s.id)
  AND NOT EXISTS (
    SELECT 1 FROM scores x JOIN limits l ON l.exam_id=x.exam_id
    WHERE x.student_id=s.id AND (x.score=l.lo OR x.score=l.hi)
  ) ORDER BY s.id;
