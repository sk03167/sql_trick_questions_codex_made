WITH points AS (
  SELECT first_player AS player_id,first_score AS score FROM matches
  UNION ALL SELECT second_player,second_score FROM matches
), totals AS (
  SELECT p.id,p.group_id,COALESCE(SUM(x.score),0) AS score
  FROM players p LEFT JOIN points x ON x.player_id=p.id GROUP BY p.id,p.group_id
), ranked AS (
  SELECT *,ROW_NUMBER() OVER (PARTITION BY group_id ORDER BY score DESC,id) AS rn FROM totals
)
SELECT group_id,id AS winner_id,score FROM ranked WHERE rn=1 ORDER BY group_id;
