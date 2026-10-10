SELECT q.turn,q.name FROM queue q
WHERE (SELECT SUM(p.weight) FROM queue p WHERE p.turn<=q.turn)<=1000
ORDER BY q.turn DESC LIMIT 1;
