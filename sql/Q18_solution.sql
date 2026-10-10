SELECT f.id,v.label
FROM facts f LEFT JOIN versions v
  ON v.key_id=f.key_id AND f.at>=v.valid_from
 AND (f.at<v.valid_to OR v.valid_to IS NULL)
ORDER BY f.id;
