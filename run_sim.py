import time
import datetime
import pandas as pd
import numpy as np   

import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import sys_configs

import configs

import production.scheduling_lib as slib

import pymysql 
conn = pymysql.connect(host=sys_configs.HOST, user=sys_configs.USER, passwd=sys_configs.PASSWD, db=sys_configs.DB)
cur = conn.cursor(pymysql.cursors.DictCursor)

uid = 'DGU'
tid = 'T1'

now_date = datetime.datetime.now().strftime('%Y-%m-%d')
weekday_list = ['mon','tue','wed','thu','fri','sat','sun']
weekday = (weekday_list[datetime.datetime.now().weekday()])


# production ###########################################
print(f'production results' + ('-'*10))

cur.execute("select TYPE, SCHEDULE, JOBS from PRODUCTIONS where UID=%s and TID=%s and PDATE=%s", (uid, tid, now_date))
data_list = cur.fetchall()
if len(data_list) > 0:    

    # qty
    # 요일에 따른 파일 선택
    ptime_file = 'production/t_500_20_'+weekday+'.csv'

    # 생산량 결정 (job 수) 1 job = 1,000 item
    # numJobs = int(np.ceil(data_list[0]['JOBS']/configs.NUM_ITEMS_PER_JOB)*configs.NUM_ITEMS_PER_JOB)    
    numJobs = data_list[0]['JOBS']
    numItems = numJobs * configs.NUM_ITEMS_PER_JOB
    print(f'\tptime_file: {ptime_file}')
    ptimes = pd.read_csv(ptime_file, index_col='JobID', nrows=numJobs)

    # SPT scheduler
    job_seq = ptimes.sort_values(by=['M1'], ascending=True).index.values
    schedule = slib.build_schedule(job_seq, ptimes)

    # makespan 계산
    makespan = schedule.iloc[-1, -1]
    print(f'\tmakespan: {makespan}, job_seq: {job_seq}')


    # gantt 저장
    fig = slib.plot_gantt_chart(schedule, figsize=(50,30), fontsize=20, outfile='gantt_chart.png')    
    fig.savefig(f'static/gantt_charts/{uid}_{tid}_{now_date}.png')    

    sql = """UPDATE PRODUCTIONS SET QTY=%s, MAKESPAN=%s, STATUS='PRODUCED' WHERE UID=%s AND TID=%s AND PDATE=%s"""
    cur.execute(sql,(numItems, makespan, uid, tid, now_date))

    sql = """INSERT INTO    INVENTORY(UID, TID, PROD_DATE, QTY)
                    VALUES (%s, %s, %s, %s)
                    ON DUPLICATE KEY UPDATE QTY=VALUES(QTY)"""
    cur.execute(sql,(uid, tid, now_date, numItems))

    # 장부
    sql = """INSERT INTO    LEDGER(UID, TID, DATE, AMOUNT, ACT, DES, SEQ)
                        VALUES (%s, %s, %s, %s, %s, %s, 1)
                        ON DUPLICATE KEY UPDATE AMOUNT=VALUES(AMOUNT), DES=VALUES(DES)"""
    # 생산비용계산
    ext_ratio = max(0.0, makespan / configs.MAKESPAN_CAPA - 1.0) # 기준 capa 대비 초과 makespan 
    prod_cost = numItems * configs.PROD_COST_UNIT
    ext_cost = ext_ratio/(ext_ratio+1.0) * prod_cost * configs.EXT_PROD_COST
    labor_cost = int(makespan/100) * configs.LABOR_COST
    print(f'prod_cost: {prod_cost}, ext_cost: {ext_cost}, labor_cost: {labor_cost}, configs.PROD_SETUP_COST: {configs.PROD_SETUP_COST}, ')
    amount = -1 * (prod_cost + ext_cost + labor_cost + configs.PROD_SETUP_COST)
    cur.execute(sql,(uid, tid, now_date, amount, 'PROD', str(numItems)+' items'))

    print('\tproduction', numItems, amount)


# sales ###########################################
print(f'sales results' + ('-'*10))

total_demand = 0
total_sales = 0
normal_sales = 0
disc_sales = 0
EXT_PRICE_PER_UNIT = 0

sql = """SELECT D.DATE as DAT, D.PRICE as DEMAND, IFNULL(S.DISC_RATIO, 0) AS DISC_RATIO, 
		 		IFNULL(ROUND(D.PRICE*S.DISC_RATIO), 0) AS EXT_DEMAND
                FROM DEMANDS AS D LEFT JOIN SALES AS S 
                ON D.DATE = S.PDATE AND S.UID = %s AND S.TID=%s 
                WHERE D.DATE=%s """
cur.execute(sql,(uid, tid, now_date))
data_list = cur.fetchall()

if len(data_list) > 0:
    # 판매량 계산 
    total_demand = int(data_list[0]['DEMAND'] + data_list[0]['EXT_DEMAND'])
    
    sql = '''
        SELECT PROD_DATE, QTY FROM INVENTORY WHERE UID=%s AND TID=%s AND QTY>0 AND
                date_format(PROD_DATE, '%%Y-%%m-%%d') <= %s ORDER BY PROD_DATE ASC
    '''
    cur.execute(sql, (uid, tid, now_date))
    inven_list = cur.fetchall()
    print('\tinventory', uid, tid, inven_list)
    
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
    # total_demand는 총수요(일반+할일)에서 판매 못하고 남은 수요 반영

    # 가격 계산
    EXT_PRICE_PER_UNIT = round((1-data_list[0]['DISC_RATIO'])*configs.PRICE_PER_UNIT)
    # 최종 판매된 일반 / 할인 제품 수
    normal_sales = min(data_list[0]['DEMAND'], total_sales)
    disc_sales = max(0, total_sales - data_list[0]['DEMAND'])

# 장부
sql = """INSERT INTO    LEDGER(UID, TID, DATE, AMOUNT, ACT, DES, SEQ)
                    VALUES (%s, %s, %s, %s, %s, %s, 3)
                    ON DUPLICATE KEY UPDATE AMOUNT=VALUES(AMOUNT), DES=VALUES(DES)"""

print(f'\tnormal_sales:{normal_sales}, disc_sales:{disc_sales}, EXT_PRICE_PER_UNIT:{EXT_PRICE_PER_UNIT}')
cur.execute(sql,(uid, tid, now_date, normal_sales*EXT_PRICE_PER_UNIT, 'SALES', str(normal_sales)+' items * $' + str(EXT_PRICE_PER_UNIT)))
cur.execute(sql,(uid, tid, now_date, disc_sales*EXT_PRICE_PER_UNIT, 'SALESD', str(disc_sales)+' discounted * $' + str(EXT_PRICE_PER_UNIT)))


# back order
# 장부
sql = """INSERT INTO    LEDGER(UID, TID, DATE, AMOUNT, ACT, DES, SEQ)
                    VALUES (%s, %s, %s, %s, %s, %s, 5)
                    ON DUPLICATE KEY UPDATE AMOUNT=VALUES(AMOUNT), DES=VALUES(DES)"""
amount = -1 *  (total_demand * configs.BACK_COST_UNIT)
cur.execute(sql,(uid, tid, now_date, amount, 'BACK', str(total_demand)+' items'))
print(f'\tback total_demand(판매후 부족수요):{total_demand}, $:{amount}')


# inventory ###########################################
print(f'inventory results' + ('-'*10))

sql = '''
    SELECT IFNULL(SUM(QTY), 0) AS INVEN FROM INVENTORY WHERE UID=%s AND TID=%s AND QTY>0
'''
cur.execute(sql, (uid, tid))
inven = cur.fetchall()[0]['INVEN']
print('\tinventory processing', uid, tid, inven)
# 장부
sql = """INSERT INTO    LEDGER(UID, TID, DATE, AMOUNT, ACT, DES, SEQ)
                    VALUES (%s, %s, %s, %s, %s, %s, 7)
                    ON DUPLICATE KEY UPDATE AMOUNT=VALUES(AMOUNT), DES=VALUES(DES)"""
amount = -1 * (inven * configs.INV_COST_UNIT)
cur.execute(sql,(uid, tid, now_date, amount, 'INVEN', str(inven)+' items'))


conn.commit()

conn.close()
