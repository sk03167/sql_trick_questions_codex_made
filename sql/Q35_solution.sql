SELECT c.day_no,(
  SELECT COUNT(DISTINCT a.user_id) FROM activity a
  WHERE a.day_no BETWEEN c.day_no-2 AND c.day_no
) AS active_users FROM calendar c ORDER BY c.day_no;
