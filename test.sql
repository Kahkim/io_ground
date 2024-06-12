INSERT INTO Test(TYPE, Contents) VALUES ('bb','Ante3333lope') ON DUPLICATE KEY UPDATE type='bb';


INSERT INTO    DEMANDS(DCODE, DATE, PRICE)
                        VALUES ('005930', '1996-07-06', 700)
                        ON DUPLICATE KEY UPDATE PRICE=VALUES(PRICE)
                        
                        
select COUNT(*) from DEMANDS