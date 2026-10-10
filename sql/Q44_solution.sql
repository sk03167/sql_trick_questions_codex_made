SELECT u.signup_day,ROUND(AVG(CASE WHEN EXISTS (
  SELECT 1 FROM activity a WHERE a.user_id=u.id AND a.day_no=u.signup_day+1
) THEN 1.0 ELSE 0.0 END),2) AS retention
FROM users u GROUP BY u.signup_day ORDER BY u.signup_day;
