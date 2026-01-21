SET TIMING ON; --timp executie
SET AUTOTRACE ON;
SELECT DISTINCT 
    colleague.name AS Mentor, 
    cert.name AS Skill_Lipsa, 
    uni.name AS Facultate
FROM USERS me
JOIN STUDIED_AT sa_me ON me.user_id = sa_me.user_id
JOIN UNIVERSITIES uni ON sa_me.uni_id = uni.uni_id
JOIN STUDIED_AT sa_col ON uni.uni_id = sa_col.uni_id
JOIN USERS colleague ON sa_col.user_id = colleague.user_id
JOIN EARNED e ON colleague.user_id = e.user_id
JOIN CERTIFICATIONS cert ON e.cert_id = cert.cert_id
WHERE me.user_id = 'u1' 
  AND colleague.user_id <> 'u1'
  AND cert.cert_id NOT IN (
      SELECT cert_id FROM EARNED WHERE user_id = 'u1'
  );
  
EXPLAIN PLAN FOR
SELECT DISTINCT colleague.name, cert.name, uni.name
FROM USERS me
JOIN STUDIED_AT sa_me ON me.user_id = sa_me.user_id
JOIN UNIVERSITIES uni ON sa_me.uni_id = uni.uni_id
JOIN STUDIED_AT sa_col ON uni.uni_id = sa_col.uni_id
JOIN USERS colleague ON sa_col.user_id = colleague.user_id
JOIN EARNED e ON colleague.user_id = e.user_id
JOIN CERTIFICATIONS cert ON e.cert_id = cert.cert_id
WHERE me.user_id = 'u1' 
  AND colleague.user_id <> 'u1'
  AND cert.cert_id NOT IN (SELECT cert_id FROM EARNED WHERE user_id = 'u1');

SELECT * FROM TABLE(DBMS_XPLAN.DISPLAY);