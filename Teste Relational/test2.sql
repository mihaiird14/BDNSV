SET TIMING ON;
SET AUTOTRACE ON;

SELECT u.name AS Prieten_Comun
FROM USERS u
JOIN FOLLOWS f1 ON u.user_id = f1.followed_id
JOIN FOLLOWS f2 ON u.user_id = f2.followed_id
WHERE LOWER(f1.follower_id) = 'u1' 
  AND LOWER(f2.follower_id) = 'u2';

EXPLAIN PLAN FOR
SELECT u.name FROM USERS u
JOIN FOLLOWS f1 ON u.user_id = f1.followed_id
JOIN FOLLOWS f2 ON u.user_id = f2.followed_id
WHERE f1.follower_id = 'u1' AND f2.follower_id = 'u2';

SELECT * FROM TABLE(DBMS_XPLAN.DISPLAY);