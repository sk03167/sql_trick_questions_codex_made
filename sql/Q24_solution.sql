SELECT o.id AS id,CASE WHEN n.id IS NULL THEN 'removed' ELSE 'changed' END AS change_kind,
       o.val AS old_value,n.val AS new_value
FROM old_snapshot o LEFT JOIN new_snapshot n ON n.id=o.id
WHERE n.id IS NULL OR o.val<>n.val
   OR (o.val IS NULL AND n.val IS NOT NULL)
   OR (o.val IS NOT NULL AND n.val IS NULL)
UNION ALL
SELECT n.id,'added',NULL,n.val
FROM new_snapshot n LEFT JOIN old_snapshot o ON o.id=n.id
WHERE o.id IS NULL
ORDER BY id;
