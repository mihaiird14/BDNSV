SET TIMING ON;
SET AUTOTRACE ON;
EXPLAIN PLAN FOR
SELECT 
    u1.role,
    COUNT(*) AS total_iteratii_simulate,
    AVG(u1.open_to_work + u2.open_to_work + u3.open_to_work + u4.open_to_work + u5.open_to_work + u6.open_to_work) AS scor_agregat
FROM USERS u1
CROSS JOIN USERS u2
CROSS JOIN USERS u3
CROSS JOIN USERS u4
CROSS JOIN USERS u5
CROSS JOIN USERS u6
GROUP BY u1.role;

-- Afi?area structurii interne de execu?ie
SELECT * FROM TABLE(DBMS_XPLAN.DISPLAY);