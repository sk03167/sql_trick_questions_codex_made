SELECT DISTINCT v.user_id FROM events v
WHERE v.kind='view' AND EXISTS (
  SELECT 1 FROM events a WHERE a.user_id=v.user_id AND a.kind='add' AND a.at>v.at
    AND EXISTS (
      SELECT 1 FROM events b WHERE b.user_id=a.user_id AND b.kind='buy' AND b.at>a.at
    )
) ORDER BY v.user_id;
