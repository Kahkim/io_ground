INSERT INTO Test(TYPE, Contents) VALUES ('bb','Ante3333lope') ON DUPLICATE KEY UPDATE type='bb';


INSERT INTO    DEMANDS(DCODE, DATE, PRICE)
                        VALUES ('005930', '1996-07-06', 700)
                        ON DUPLICATE KEY UPDATE PRICE=VALUES(PRICE)
                        
                        
DESC DEMAND_FOR

SELECT * FROM DEMANDS ORDER BY DATE DESC


SELECT D.DATE, D.PRICE, F.DEMAND_FOR
FROM DEMANDS AS D LEFT JOIN DEMAND_FOR AS F 
ON D.DATE = F.PDATE AND F.UID = 'DGU' AND F.TID='T1'
ORDER BY D.DATE DESC LIMIT 10

WHERE F.UID = 'DGU' AND F.TID='T1'

SELECT * FROM DEMANDS AS D, DEMAND_FOR AS F
WHERE D.DATE = F.PDATE

WHERE F.UID = 'DGU' AND F.TID='T1'


        SELECT D.DATE as DAT, D.PRICE as ACT, IFNULL(S.DISC_RATIO, 0) AS DISC_RATIO, 
		  			IFNULL(ROUND(D.PRICE*S.DISC_RATIO), 0)
        FROM DEMANDS AS D LEFT JOIN SALES AS S 
        ON D.DATE = S.PDATE AND S.UID = 'DGU' AND S.TID='T1' 
        WHERE D.DATE='2024-07-16'
        ORDER BY D.DATE DESC LIMIT 10

SELECT * FROM DEMAND_FOR
WHERE UID = 'DGU' AND TID='T1' AND PDATE > NOW()
ORDER BY PDATE ASC

SELECT PDATE, SCHEDULE FROM PRODUCTIONS
WHERE UID = 'DGU' AND TID='T1'

SELECT * from INVENTORY WHERE UID = 'DGU' AND TID = 'T1' AND QTY>0

SELECT SUM(QTY) AS INVEN FROM INVENTORY


SELECT sum(QTY) FROM INVENTORY WHERE QTY>0 AND
            PROD_DATE < '2024-07-16'