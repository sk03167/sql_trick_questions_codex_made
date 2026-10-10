WITH positioned AS (
  SELECT *,ROW_NUMBER() OVER (ORDER BY seat_id) AS pos FROM seats
)
SELECT a.seat_id,COALESCE(b.occupant,a.occupant) AS occupant
FROM positioned a LEFT JOIN positioned b
  ON b.pos=CASE WHEN a.pos%2=1 THEN a.pos+1 ELSE a.pos-1 END
ORDER BY a.seat_id;
