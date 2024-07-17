import time
import datetime
import pandas as pd
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import sys_configs

import configs

import pymysql 
conn = pymysql.connect(host=sys_configs.HOST, user=sys_configs.USER, passwd=sys_configs.PASSWD, db=sys_configs.DB)
cur = conn.cursor(pymysql.cursors.DictCursor)

uid = 'DGU'
tid = 'T1'

now_date = datetime.datetime.now().strftime('%Y-%m-%d')

# sales ###########################################

sql = """SELECT D.DATE as DAT, D.PRICE as DEMAND, IFNULL(S.DISC_RATIO, 0) AS DISC_RATIO, 
		 		IFNULL(ROUND(D.PRICE*S.DISC_RATIO), 0) AS EXT_DEMAND
                FROM DEMANDS AS D LEFT JOIN SALES AS S 
                ON D.DATE = S.PDATE AND S.UID = %s AND S.TID=%s 
                WHERE D.DATE=%s """
cur.execute(sql,(uid, tid, now_date))
data_list = cur.fetchall()
if len(data_list) > 0:
    # 판매량 계산 
    total_demand = data_list[0]['DEMAND'] + data_list[0]['EXT_DEMAND']
    
    sql = '''
        SELECT PROD_DATE, QTY FROM INVENTORY WHERE UID=%s AND TID=%s AND QTY>0 AND
                PROD_DATE < %s ORDER BY PROD_DATE ASC
    '''
    cur.execute(sql, (uid, tid, now_date))
    inven_list = cur.fetchall()
    print('inventory', uid, tid, inven_list)

    total_sales = 0
    for il in inven_list:        
        sales_qty = min(total_demand, il['QTY'])
        sql = '''
            UPDATE INVENTORY SET QTY=%s WHERE UID=%s AND TID=%s AND PROD_DATE=%s
        '''        
        cur.execute(sql, (il['QTY']-sales_qty, uid, tid, il['PROD_DATE']))
        total_demand = total_demand - sales_qty
        total_sales = total_sales + sales_qty
        # print(sales_qty, il['QTY']-sales_qty, il['PROD_DATE'], total_demand)
        if total_demand<=0:
            break    

    # 장부
    # 가격 계산
    EXT_PRICE_PER_UNIT = round((1-data_list[0]['DISC_RATIO'])*configs.PRICE_PER_UNIT)
    sql = """INSERT INTO    LEDGER(UID, TID, DATE, AMOUNT, ACT, DES, SEQ)
                        VALUES (%s, %s, %s, %s, %s, %s, 0)
                        ON DUPLICATE KEY UPDATE AMOUNT=VALUES(AMOUNT), DES=VALUES(DES)"""
    normal_sales = min(data_list[0]['DEMAND'], total_sales)
    disc_sales = max(0, total_sales - data_list[0]['DEMAND'])
    print('sales results', uid, tid, normal_sales, configs.PRICE_PER_UNIT, disc_sales, EXT_PRICE_PER_UNIT)
    print(str(normal_sales)+' items')
    cur.execute(sql,(uid, tid, now_date, normal_sales*configs.PRICE_PER_UNIT, 'SALES', str(normal_sales)+' items'))
    cur.execute(sql,(uid, tid, now_date, disc_sales*EXT_PRICE_PER_UNIT, 'SALESD', str(disc_sales)+' discounted'))


# inventory ###########################################

sql = '''
    SELECT IFNULL(SUM(QTY), 0) AS INVEN FROM INVENTORY WHERE UID=%s AND TID=%s AND QTY>0 AND PROD_DATE<%s
'''
cur.execute(sql, (uid, tid, now_date))
inven = cur.fetchall()[0]['INVEN']
print('inventory processing', uid, tid, inven)
# 장부
sql = """INSERT INTO    LEDGER(UID, TID, DATE, AMOUNT, ACT, DES, SEQ)
                    VALUES (%s, %s, %s, %s, %s, %s, 3)
                    ON DUPLICATE KEY UPDATE AMOUNT=VALUES(AMOUNT), DES=VALUES(DES)"""
amount = -1 * (inven * configs.INV_COST_UNIT)
cur.execute(sql,(uid, tid, now_date, amount, 'INVEN', str(inven)+' items'))

# back order
# 장부
sql = """INSERT INTO    LEDGER(UID, TID, DATE, AMOUNT, ACT, DES, SEQ)
                    VALUES (%s, %s, %s, %s, %s, %s, 5)
                    ON DUPLICATE KEY UPDATE AMOUNT=VALUES(AMOUNT), DES=VALUES(DES)"""
amount = -1 *  (total_demand * configs.BACK_COST_UNIT)
cur.execute(sql,(uid, tid, now_date, amount, 'BACK', str(total_demand)+' items'))
print('back', uid, tid, total_demand, amount)

# production ###########################################
cur.execute("select TYPE, SCHEDULE, QTY from PRODUCTIONS where UID=%s and TID=%s and PDATE=%s", (uid, tid, now_date))
data_list = cur.fetchall()
if len(data_list) > 0:    
    sql = """INSERT INTO    INVENTORY(UID, TID, PROD_DATE, QTY)
                    VALUES (%s, %s, %s, %s)
                    ON DUPLICATE KEY UPDATE QTY=VALUES(QTY)"""
    cur.execute(sql,(uid, tid, now_date, data_list[0]['QTY']))

    # 장부
    sql = """INSERT INTO    LEDGER(UID, TID, DATE, AMOUNT, ACT, DES, SEQ)
                        VALUES (%s, %s, %s, %s, %s, %s, 7)
                        ON DUPLICATE KEY UPDATE AMOUNT=VALUES(AMOUNT), DES=VALUES(DES)"""
    amount = -1 * (data_list[0]['QTY'] * configs.PROD_COST_UNIT + configs.PROD_SETUP_COST)
    cur.execute(sql,(uid, tid, now_date, amount, 'PROD', str(data_list[0]['QTY'])+' items'))

    print('production', uid, tid, data_list[0]['QTY'], amount)


conn.commit()

conn.close()
