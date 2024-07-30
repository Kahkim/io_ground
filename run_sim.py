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

# 전개 초기화
sql = """DELETE FROM INVENTORY_HIST WHERE UID=%s AND TID=%s AND date_format(PROD_DATE, '%%Y-%%m-%%d')>=%s"""
cur.execute(sql,(uid, tid, now_date))
sql = """DELETE FROM LEDGER WHERE UID=%s AND TID=%s AND date_format(DATE, '%%Y-%%m-%%d')>=%s"""
cur.execute(sql,(uid, tid, now_date))

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
    ptimes = pd.read_csv(ptime_file, index_col='JobID', nrows=numJobs)
    makespan = 0
    setup_cost = 0
    
    # job seq
    job_seq = ptimes.sort_values(by=['M1'], ascending=True).index.values

    if len(job_seq)>0:
        # SPT scheduler    
        schedule = slib.build_schedule(job_seq, ptimes)
        # print(schedule)
        # makespan 계산
        makespan = schedule.iloc[-1, -1]
        # setup cost 계산
        setup_cost = configs.PROD_SETUP_COST
        # gantt 저장
        fig = slib.plot_gantt_chart(schedule, figsize=(50,30), fontsize=20, outfile='gantt_chart.png')    
        fig.savefig(f'static/gantt_charts/{uid}_{tid}_{now_date}.png')    

    print(f'\tptime_file: {ptime_file}, makespan: {makespan}, job_seq: {job_seq}')

    sql = """UPDATE PRODUCTIONS SET QTY=%s, MAKESPAN=%s, STATUS='PRODUCED' WHERE UID=%s AND TID=%s AND PDATE=%s"""
    cur.execute(sql,(numItems, makespan, uid, tid, now_date))

    sql = """INSERT INTO    INVENTORY_HIST(UID, TID, PROD_DATE, PROD_QTY)
                    VALUES (%s, %s, %s, %s)
                    ON DUPLICATE KEY UPDATE PROD_QTY=VALUES(PROD_QTY)"""
    cur.execute(sql,(uid, tid, now_date, numItems))

    # 장부
    sql = """INSERT INTO    LEDGER(UID, TID, DATE, REVENUE, EXPENSE, ACT, DES, SEQ)
                        VALUES (%s, %s, %s, 0, %s, %s, %s, 1)
                        ON DUPLICATE KEY UPDATE REVENUE=VALUES(REVENUE), EXPENSE=VALUES(EXPENSE), DES=VALUES(DES)"""
    # 생산비용계산
    ext_ratio = max(0.0, makespan / configs.MAKESPAN_CAPA - 1.0) # 기준 capa 대비 초과 makespan 
    prod_cost = numItems * configs.PROD_COST_UNIT
    ext_cost = ext_ratio/(ext_ratio+1.0) * prod_cost * configs.EXT_PROD_COST
    labor_cost = int(makespan/100) * configs.LABOR_COST
    
    print(f'''\tprod_cost: {prod_cost}, ext_cost: {ext_cost}, labor_cost: {labor_cost}, 
          configs.PROD_SETUP_COST: {setup_cost}, ''')
    amount = -1 * (prod_cost + ext_cost + labor_cost + setup_cost)
    cur.execute(sql,(uid, tid, now_date, amount, 'PROD', str(numItems)+' items'))

    print(f'\t#items: {numItems}, amount: {amount}')


# sales ###########################################
print(f'sales results' + ('-'*10))

total_demand = 0
total_sales = 0
# normal_sales = 0
# disc_sales = 0
FIN_PRICE_PER_UNIT = configs.PRICE_PER_UNIT

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
        SELECT PROD_DATE, PROD_QTY, SUM(SALES_QTY), PROD_QTY-SUM(SALES_QTY) AS REMAINS_QTY 
        from INVENTORY_HIST 
        WHERE UID=%s AND TID=%s AND date_format(PROD_DATE, '%%Y-%%m-%%d')<=%s
        GROUP BY UID, TID, PROD_DATE
        HAVING REMAINS_QTY > 0
        ORDER BY PROD_DATE ASC '''
    cur.execute(sql, (uid, tid, now_date))
    inven_list = cur.fetchall()
    print('\tinventory', uid, tid, inven_list)

    # 가격 계산
    FIN_PRICE_PER_UNIT = round((1-data_list[0]['DISC_RATIO'])*configs.PRICE_PER_UNIT)

    for il in inven_list:        
        sales_qty = min(total_demand, il['REMAINS_QTY']) # inven에서 꺼내는 수
        sql = '''
            INSERT INTO INVENTORY_HIST(UID, TID, PROD_DATE, PROD_QTY, SALES_DATE, SALES_QTY)
            VALUES (%s, %s, %s, 0, %s, %s)
            ON DUPLICATE KEY UPDATE SALES_QTY=VALUES(SALES_QTY)
        '''        
        cur.execute(sql, (uid, tid, il['PROD_DATE'], now_date, sales_qty))
        total_demand = total_demand - sales_qty # total_demand는 총수요(일반+할일)에서 판매 못하고 남은 수요 반영
        total_sales = total_sales + sales_qty # 현재까지 inven에서 꺼낸 총 수
        # print(sales_qty, il['QTY']-sales_qty, il['PROD_DATE'], total_demand)
        
        # 최종 판매된 일반 / 할인 제품 수
        # normal_sales = min(data_list[0]['DEMAND'], total_sales)
        # disc_sales = max(0, total_sales - data_list[0]['DEMAND'])        

        if total_demand<=0:
            break    
    
    # 장부
    sql = """INSERT INTO    LEDGER(UID, TID, DATE, REVENUE, ACT, DES, SEQ)
                        VALUES (%s, %s, %s, %s, %s, %s, 3)
                        ON DUPLICATE KEY UPDATE REVENUE=VALUES(REVENUE), DES=VALUES(DES)"""

    print(f'\ttotal_sales:{total_sales}, total_demand:{total_demand}, FIN_PRICE_PER_UNIT:{FIN_PRICE_PER_UNIT}')
    cur.execute(sql,(uid, tid, now_date, 
                        total_sales*FIN_PRICE_PER_UNIT, 
                        f'SALES', 
                        str(total_sales)+' items * $' + str(FIN_PRICE_PER_UNIT)))
    

# back order
# 장부
sql = """INSERT INTO    LEDGER(UID, TID, DATE, EXPENSE, ACT, DES, SEQ)
                    VALUES (%s, %s, %s, %s, %s, %s, 5)
                    ON DUPLICATE KEY UPDATE EXPENSE=VALUES(EXPENSE), DES=VALUES(DES)"""
amount = -1 *  (total_demand * configs.BACK_COST_UNIT)
cur.execute(sql,(uid, tid, now_date, amount, 'BACK', str(total_demand)+' items * $' + str(configs.BACK_COST_UNIT)))
print(f'\tback total_demand:{total_demand}, $:{amount}')


# inventory ###########################################
print(f'inventory results' + ('-'*10))

sql = '''
    SELECT SUM(AA.REMAINS_QTY) as REMAINS_QTY FROM (
    SELECT PROD_DATE, PROD_QTY, SUM(SALES_QTY), PROD_QTY-SUM(SALES_QTY) AS REMAINS_QTY 
    from INVENTORY_HIST 
    WHERE UID=%s AND TID=%s
    GROUP BY UID, TID, PROD_DATE
    ) AA    
'''
cur.execute(sql, (uid, tid))
inven = cur.fetchall()[0]['REMAINS_QTY']
print(f'\t#items: {inven}')
# 장부
sql = """INSERT INTO    LEDGER(UID, TID, DATE, REVENUE, EXPENSE, ACT, DES, SEQ)
                    VALUES (%s, %s, %s, 0, %s, %s, %s, 7)
                    ON DUPLICATE KEY UPDATE REVENUE=VALUES(REVENUE), EXPENSE=VALUES(EXPENSE), DES=VALUES(DES)"""
amount = -1 * (inven * configs.INV_COST_UNIT)
cur.execute(sql,(uid, tid, now_date, amount, 'INVEN', str(inven)+' items * $' + str(configs.INV_COST_UNIT)))


conn.commit()

conn.close()
