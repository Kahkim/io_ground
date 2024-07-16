import pymysql
conn = pymysql.connect(host='192.168.0.3', user='io_ground', passwd='dkshk24@!', db='io_ground')

cur = conn.cursor()

sql = '''
    SELECT SUM(QTY) AS INVEN FROM INVENTORY WHERE UID=%s AND TID=%s AND QTY>0 AND PROD_DATE<%s
'''
print(sql, ('DGU', 'T1', '2024-07-16'))
cur.execute(sql, ('DGU', 'T1', '2024-07-16'))
inven = cur.fetchall()
print(inven)


conn.close()

import datetime

date = datetime.datetime.strptime('2024-06-12', '%Y-%m-%d')
print(date.weekday())

next_day_date = date + datetime.timedelta(days=1)
print(next_day_date)


now = datetime.datetime.now()
print(now)
next_day_date = now + datetime.timedelta(days=1)
print(next_day_date)
next_day_date = now + datetime.timedelta(days=2)
print(next_day_date)





